from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as Login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from datetime import datetime, date
from django.db.models import Count
from config.settings import redis
from django.core.cache import cache
from .forms import LoginForm, RegisterForm
from django.db import IntegrityError


class LoginView(View):
    
    def get(self, request):
        form = LoginForm
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        remember = request.POST.get('rememberme')
        if form.is_valid():
            cd =  form.cleaned_data
            if '@' in cd.get('username'):
                user = User.objects.get(email=cd['username'])
            else:
                user = User.objects.get(username=cd['username'])
            if user and user.check_password(cd['password']):
                login(request, user)
                if remember:
                    request.session.set_expiry(0)
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('user_panel')
            else:
                form.add_error('password', 'نام کاربری یا گذرواژه اشتباه است')
                
        return render(request, 'login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST, initial=request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
            except IntegrityError:
                pass
        return render(request, 'register.html', {'form': form})