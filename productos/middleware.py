from django.shortcuts import redirect

class AutorizaciónMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != '/login/':
            return redirect('login')
        return self.get_response(request)
    
import datetime

class LogsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #antes de lka vista
        print(f"Nueva Solicitud: Metodo: {request.method}, URL: {request.path}, Hora: {datetime.datetime.now()}")

        response = self.get_response(request)
        #después de la vista
        print(f"Respuesta: {response.status_code}, Hora: {datetime.datetime.now()}")
        return response