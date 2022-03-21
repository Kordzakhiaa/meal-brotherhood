from functools import wraps
from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect


def function():
    return type(function)


def restrict_access(func: 'function') -> Union[function, HttpResponsePermanentRedirect, HttpResponseRedirect]:
    """
    Decorator for authenticated users to restrict some endpoints
    for example: (login, register)...
    """
    @wraps(func)
    def wrap(request: WSGIRequest):
        if request.user.is_authenticated:
            return redirect('meal_brotherhood:home')

    return wrap
