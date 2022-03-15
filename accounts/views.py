from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from accounts.forms import CreateUserForm
from accounts.models import Account


class HomeView(View):
    def get(self, request):
        return render(request, 'meal_brotherhood/index.html')

    def post(self, request):
        pass


class GetPerm(View):
    def get(self, request):
        user = Account.objects.get(id=request.user.id)
        user.want_food = True
        user.save()
        return redirect('accounts:home')


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'account/register.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:login')


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
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username or Password is incorrect')
        return render(request, 'account/login.html')


def logout_page(request):
    logout(request)
    return redirect('user:login_page')
