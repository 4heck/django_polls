from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from polls.models import Poll


def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.values("title", "pub_date").annotate(
        created_by=F("created_by__username")
    )
    results = polls[:MAX_OBJECTS]
    data = {"results": list(results)}
    return JsonResponse(data)


def polls_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {
        "results": {
            "question": poll.title,
            "created_by": poll.created_by.username,
            "pub_date": poll.pub_date,
        }
    }
    return JsonResponse(data)
