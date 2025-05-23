from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login/'):
            if not request.user.is_authenticated:
                return redirect(f'/admin/login/?next={request.path}')
            if not request.user.is_staff:
                return HttpResponseForbidden("Доступ запрещен")
        return None