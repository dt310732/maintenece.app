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
                "created_at": message.created_at.isoformat(),
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
        
        # text-pole z modelu Message i text-z jsona 
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

def message_details(request: HttpRequest, message_id: int) -> JsonResponse:
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return JsonResponse(
            {"error": "Message not found"},
            status = 404,
        )

    if request.method == "DELETE":
        deleted_id = message.id
        message.delete()

        return JsonResponse({
            "deleted": True,
            "id": deleted_id,
        }, status = 200,
        )
    
    return JsonResponse(
        {"erorr": "Method not allowed"},
        status = 405,
    )