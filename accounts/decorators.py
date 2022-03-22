from functools import wraps
from types import FunctionType
from typing import Union

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render


def restrict_access(func: FunctionType) -> Union[FunctionType, HttpResponsePermanentRedirect, HttpResponseRedirect]:
    """
    Decorator for authenticated users to restrict some endpoints
    for example: (login, register)...
    """

    @wraps(func)
    def wrapper(request: WSGIRequest) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        if request.user.is_authenticated:
            return redirect('meal_brotherhood:home')
        if request.path == '/accounts/login/':
            return render(request, 'account/login.html')
        return redirect('accounts:register')

    return wrapper  # noqa
