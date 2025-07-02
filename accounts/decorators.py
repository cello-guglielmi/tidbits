from functools import wraps
from django.contrib.auth.views import redirect_to_login

'''
# Could have alternatively written a lightweight middleware to check for every request
class EnforceActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            from django.contrib.auth import logout
            from django.shortcuts import redirect
            logout(request)
            return redirect('login')  # or redirect_to_login(request.get_full_path())
        return self.get_response(request)
'''

def active_login_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = getattr(request, 'user', None) # = request.user
        if not (user and user.is_authenticated and user.is_active):
            return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapped