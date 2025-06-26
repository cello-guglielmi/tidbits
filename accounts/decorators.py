from functools import wraps
from django.contrib.auth.views import redirect_to_login

def active_login_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = getattr(request, 'user', None) # = request.user
        if not (user and user.is_authenticated and user.is_active):
            return redirect_to_login(request.get_full_path())
        return view_func(request, *args, **kwargs)
    return wrapped