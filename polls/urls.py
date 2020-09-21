from django.urls import path, re_path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from polls.apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate
from django.conf import settings


router = DefaultRouter()
router.register("polls", PollViewSet, basename="polls")


urlpatterns = [
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path(
        "polls/<int:pk>/choices/<int:choice_pk>/vote/",
        CreateVote.as_view(),
        name="create_vote",
    ),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", views.obtain_auth_token, name="login"),
]

urlpatterns += router.urls

if settings.DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version="v1",
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
