from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings


def unauthenticated_user(view_func, redirect_url=None):
    """
    Redirects authenticated users to the specified URL.
    Allows only unauthenticated users to access the decorated view.

    :param redirect_url: URL to redirect authenticated users to (defaults to LOGIN_REDIRECT_URL or '/')
    """
    if redirect_url is None:
        redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', '/')

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_url)  # Redirect authenticated users
        else:
            return view_func(request, *args, **kwargs)  # Allow unauthenticated users

    return wrapper_func

def allowed_users(allowed_groups=None, body="Access Denied"):
    """
    Allows access to the view only if the user is part of the allowed groups.
    If the user is not part of the allowed groups, they get an 'Access Denied' message.
    :param allowed_groups: List of allowed group names (e.g., ['admin', 'manager'])
    :param body: The message to display when access is denied
    """
    if allowed_groups is None:
        allowed_groups = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # Get the user's group names
            user_groups = request.user.groups.values_list('name', flat=True)

            # Check if any of the user's groups are in the allowed list
            if any(group in allowed_groups for group in user_groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(body)

        return wrapper_func

    return decorator
