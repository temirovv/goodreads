from pprint import pprint

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, UserUpdateForm


class RegisterView(View):
    def get(self, request):
        context = {
            'form': UserForm()
        }
        return render(request, 'users/register.html', context=context)  # noqa

    def post(self, request):
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            return render(request, 'users/register.html', context={'form': form})  # noqa


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', context={'form': form})  # noqa

    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect('books:books')

        else:
            messages.warning(request, 'invalid username or password')
            return render(request, 'users/login.html', context={'form': form}, status=401)  # noqa


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', context={'user': request.user})



class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out")
        return redirect('home')


class ProfileUpdateView(LoginRequiredMixin ,View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_update.html', context={'form': form})

    def post(self, request):
        form = UserUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():

            form.save()
            messages.success(request, 'Your Profile Has been successfully updated')

            return redirect('users:profile')

        return render(request, 'users/profile_update.html', {"form": form})
