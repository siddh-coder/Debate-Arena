from django.contrib.auth.decorators import login_required as django_login_required
from django.shortcuts import render
from django.http import HttpResponseForbidden

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'debate/create_debate.html', {
                'form': None,
                'error': 'You must be logged in to create a debate. Please sign up or log in to continue.'
            })
        return django_login_required(view_func)(request, *args, **kwargs)
    return wrapper
