import json
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Message

def ping(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        'status': 'ok',
        'app': 'demo'
    })


@csrf_exempt
def messages(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        messages_qs = Message.objects.order_by("-created_at")

        data = [
            {
                "id": message.id,
                "text": message.text,
                "created_ad": message.created_at.isoformat(),
            }
            for message in messages_qs
        ]

        return JsonResponse(data, safe=False)
    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )
