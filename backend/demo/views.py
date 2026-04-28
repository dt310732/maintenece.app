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
    
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Involid Json"},
                status=400,
            )
        
        text = body.get("text", "").strip()

        if not text:
            return JsonResponse(
                {"error": "Field 'text' is required"},
                status=400,
            )
        
        message = Message.objects.create(text=text)

        return JsonResponse(
            {
                "id": message.id,
                "text": message.text,
                "created_at": message.created_at.isoformat(),
            }, status = 201,
        )
    
    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )
