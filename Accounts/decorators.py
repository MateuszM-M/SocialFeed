from django.shortcuts import redirect


def unathenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Accounts:dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
