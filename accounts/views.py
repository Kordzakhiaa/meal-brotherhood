from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from accounts.forms import CreateUserForm


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)


class LoginView(View):
    def get(self, request):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'account/login.html', context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('meal_brotherhood:home')
        else:
            messages.info(request, 'Username or Password is incorrect')
        return render(request, 'account/login.html')


def logout_page(request):
    logout(request)
    return redirect('accounts:login')
