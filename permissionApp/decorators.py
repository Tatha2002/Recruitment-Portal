from functools import wraps
from django.shortcuts import render

from .models import RolePermission

def permission_required(permission_name):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            user_role = request.user.role
            permission_exists = RolePermission.objects.filter(role=user_role, permission__name=permission_name).exists()
            
            if not permission_exists:
                return render(request, "errors/403.html", status=403)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator