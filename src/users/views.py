from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as Login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.db.models import Count
from config.settings import redis
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from datetime import datetime, date
from django.contrib import messages
import requests
from requests.exceptions import ConnectionError
from django.db import transaction
import logging
from .models import User, Notification
from .tokens import email_verification_token
from .forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordCompleteForm
from payments.models import Subscribe, Payment, PaymentMethod
from home.views import get_navbar
from django.db.models import Q

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
                user = User.objects.get(email=cd['username'].strip())
            else:
                user = User.objects.get(username=cd['username'].strip())
            if user and user.check_password(cd['password'].strip()):
                login(request, user)
                if remember:
                    request.session.set_expiry(0)
                request.session.set_expiry(60 * 60 * 24 * 7)
                return redirect('user_panel')
            else:
                form.add_error('password', 'نام کاربری یا گذرواژه اشتباه است')
        return render(request, 'login.html', {'form': form}, status=400)



class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST, initial=request.POST)
        ipaddress = request.META['REMOTE_ADDR']
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.ipaddress = ipaddress
                    user.save()
                    try:   
                        requests.get(request.build_absolute_uri(reverse('send-activate-code', args=[user.pk,])))
                    except (ConnectionError) as error:
                        logging.error(f'{error} IPAddress: {ipaddress}')
                        messages.error(request, 'مشکلی در ساخت حساب شما پیش آمد بعدا امتحان کنید')
            except (IntegrityError):
                pass
        return render(request, 'register.html', {'form': form})

class ResetPasswordView(View):
    def get(self, request):
        form = ResetPasswordForm
        return render(request, 'password_reset.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        ipaddress = request.META['REMOTE_ADDR']
        if form.is_valid():
            cd = form.cleaned_data
            try:
                r = requests.post(request.build_absolute_uri(reverse('password-recovery-token')), data={'email': cd['email']})
                if r.status_code == 200:
                    messages.success(request, 'لینک بازیابی به ایمیل شما ارسال شد', 'success')
                    return redirect('password-recovery')
            except ConnectionError as error:
                logging.error(f'{error} IPAddress: {ipaddress}')
        return render(request, 'password_reset.html', {'form': form}, status=400)


class ResetPasswordCompleteView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and email_verification_token.check_token(user, token):
            form = ResetPasswordCompleteForm
            return render(request, 'password_reset_complete.html', {'form': form})
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
    
    def post(self, request, uidb64, token):
        form = ResetPasswordCompleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user and email_verification_token.check_token(user, token):
                user.set_password(cd['password1'])
                user.save()
                messages.success(request, 'رمزعبور شما با موفقیت تغییر کرد', 'success')
            return redirect('login')
        return render(request, 'password_reset_complete.html', {'form': form}, status=400)



class UserPanelView(View):
    def get(self, request):
        user = User.get_current_user
        notifications_count = Notification.get_notification_count()
        payment_methods = PaymentMethod.objects.all().values('name', 'id')
        subscribes = Subscribe.objects.all().values('name', 'price', 'discount', 'time')
        for item in subscribes:
            if item['discount']:
                item['discount'] = abs((item['price'] * item['discount'] // 100) - item['price'])
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'subscribes': subscribes,
                   'payment_methods': payment_methods,
                   }
        return render(request, 'user_panel_dashboard.html', context)