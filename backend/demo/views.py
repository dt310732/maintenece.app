from django.http import JsonResponse, HttpRequest

def ping(request: HttpRequest) -> JsonResponse:
    return JsonResponse({
        'status': 'ok',
        'app': 'demo'
    })