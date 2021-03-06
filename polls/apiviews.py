from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from polls.models import Poll, Choice
from polls.serializers import (
    PollSerializer,
    ChoiceSerializer,
    VoteSerializer,
    UserSerializer,
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs.get("pk"))
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("pk"))
        queryset = Choice.objects.filter(poll=poll)
        return queryset

    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, pk=self.kwargs.get("pk"))
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    serializer_class = VoteSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="voted_by",
                in_="query",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ]
    )
    def post(self, request, pk, choice_pk):
        voted_by = request.query_params.get("voted_by")
        data = {"choice": choice_pk, "poll": pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(
        self,
        request,
    ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
