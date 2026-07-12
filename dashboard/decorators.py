from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponse


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("admin_login")

        if not request.user.is_staff:
            return HttpResponse("Access Denied")

        return view_func(request, *args, **kwargs)

    return wrapper


def student_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.is_staff:
            return redirect("dashboard_home")

        return view_func(request, *args, **kwargs)

    return wrapper