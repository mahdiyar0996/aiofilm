from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout
from django.utils.http import  urlsafe_base64_decode
from django.db.models import Count, Sum, QuerySet, F, Case, When
from config.settings import redis
from django.core.cache import cache
from django.db import IntegrityError
from datetime import datetime
from django.contrib import messages
import requests
from requests.exceptions import ConnectionError
from django.db import transaction
import logging
from products.models import Movie
from .models import User, Notification, Ticket, TicketAdminReply, TicketDetails, Bookmark, Favorite, Comment, Reply
from .tokens import email_verification_token
from .forms import (LoginForm, RegisterForm, ResetPasswordForm,
                    ResetPasswordCompleteForm, ChangePasswordForm,
                    ChangeUserInformationForm, TicketDetailsForm, TicketForm)
from payments.models import Subscribe, Payment, PaymentMethod
from home.views import get_navbar
from django.db.models import Q
from utils.tools import get_paginator
import jdatetime


def panel_base_data(request, field=None):
    user = User.get_current_user(request, field)
    user_id = user['id']
    notifications_count = Notification.get_user_notifications_count(user_id)
    return user,user_id,notifications_count
    

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
                return redirect('user-panel')
            else:
                form.add_error('password', 'نام کاربری یا گذرواژه اشتباه است')
        return render(request, 'login.html', {'form': form}, status=400)

class LogoutView(View):
    def get(self, request):
        user_id = request.session.get('_auth_user_id')
        redis.delete(f"user-{user_id}")
        logout(request)
        return redirect('home')

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
            if user.check_password(cd['password1']):
                form.add_error('password1', 'رمز عبور نمیتواند رمز فعلی باشد')
            if user and email_verification_token.check_token(user, token):
                user.set_password(cd['password1'])
                user.last_password_reset = jdatetime.datetime.now()
                user.save()
                messages.success(request, 'رمزعبور شما با موفقیت تغییر کرد', 'success')
            return redirect('login')
        return render(request, 'password_reset_complete.html', {'form': form}, status=400)



class PanelView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        if user['subscribe'] != 'None':
            days = abs((datetime.now().date() -
                                    datetime.strptime(
                                        user['subscribe'],
                                        '%Y-%m-%d %H:%M:%S%z').date())).days
            user['subscribe'] = days
        else:
            user['subscribe'] = 0
            
        payment_methods = cache.get(f'payment-methods')
        if not payment_methods:
            payment_methods = PaymentMethod.objects.all().values('name', 'id')
            cache.set(f'payment-methods', payment_methods, 60 * 60 * 12)
            
        payments = cache.get(f'payment-{user_id}')
        if not payments:
            payments = Payment.objects.select_related('subscribe').filter(user__pk=user['id']).values(
                'price', 'subscribe__time', 'method__name', 'created_at')[:10]
            cache.set(f'payment-{user_id}', payments, 60 * 10)
        for item in payments:
            item['created_at'] = jdatetime.datetime.strptime(str(item['created_at']), '%Y-%m-%d %H:%M:%S.%f%z').date
        subscribes =  cache.get('subscribes')
        if not subscribes:
            subscribes = Subscribe.objects.all().values('name', 'price', 'discount', 'time')
            cache.set('subscribes', subscribes, 60 * 60 * 24)
        for item in subscribes:
            if item['discount']:
                item['discount'] = abs((item['price'] * item['discount'] // 100) - item['price'])
                
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'subscribes': subscribes,
                   'payments': payments,
                   'payment_methods': payment_methods,
                   }
        
        return render(request, 'user_panel_dashboard.html', context)


class PanelChangePasswordView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        form = ChangePasswordForm
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'form': form}
        return render(request, 'user_panel_change_password.html', context)


    def post(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            cd = form.cleaned_data
            if user.check_password(cd['password1']):
                form.add_error('password1', 'رمز عبور نمیتواند رمز فعلی باشد')
                
            if user.check_password(cd['password']):
                user.set_password(cd['password1'])
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
            else:
                form.add_error('password', 'رمز عبور وارد شده اشتباه است')
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'form': form}
        return render(request, 'user_panel_change_password.html', context)

class PanelEditAccountView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        form = ChangeUserInformationForm(initial=user)
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'form': form}
        return render(request, 'user_panel_change_profile.html', context)
    
    def post(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        
        user = User.objects.get(pk=user_id)
        
        form = ChangeUserInformationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.cleaned_data['email'] = user.email
            form.cleaned_data['email'] = request.POST.get('avatar') if request.POST.get('avatar') else user.avatar
            form.save()
            with redis.pipeline() as pipeline:
                pipeline.hset(f"user-{user_id}", mapping=user.to_dict())
                pipeline.expire(f"user-{user_id}", 60 * 30)
                pipeline.execute()
            return redirect('user-edit-account')
        form = ChangeUserInformationForm(initial=user.to_dict())
        
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'form': form}
        
        return render(request, 'user_panel_change_profile.html', context)


class TicketListView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        tickets = cache.get(f'tickets-{user_id}')
        if not tickets:
            tickets = Ticket.objects.filter(user__pk=user['id']).order_by(
                'created_at').values('id','department', 'subject',
                                     'admin_closed', 'user_closed',
                                     'updated_at')
            cache.set(f'tickets-{user_id}', tickets, 60 * 5)

        
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'tickets': tickets}
        return render(request, 'user_panel_ticket_list.html', context)


class TicketDetailsView(View):
    def get(self, request, id):
        user,user_id,notifications_count = panel_base_data(request)
        
        tickets_replies = cache.get(f'tickets_replies-{user_id}')
        if not tickets_replies:
            tickets_replies = TicketDetails.objects.select_related('ticket', 'user').filter(
                ticket__id=id, user__id=user_id).order_by('-created_at').values(
                'message', 'file','created_at', 'id', 'ticket__id',
                'ticket__user', 'ticket__department', 'ticket__subject', 'ticket__admin_closed', "ticket__user_closed")
            cache.set(f'tickets_replies-{user_id}', tickets_replies, 60 * 5)
            
        ticket_ids = [item['id'] for item in tickets_replies]
        ticket = tickets_replies[0]
        
        ticket_is_open = True if ticket['ticket__admin_closed'] or ticket['ticket__user_closed'] else False
        
        tickets_admin_replies = cache.get(f'tickets_admin_replies-{user_id}')
        if not tickets_admin_replies:
            tickets_admin_replies = TicketAdminReply.objects.select_related('ticket').filter(
                ticket__in=ticket_ids).order_by('-created_at').values(
                'ticket__id', 'created_at',
                'message', 'file','updated_at')
            cache.set(f'tickets_admin_replies-{user_id}', tickets_admin_replies, 60 * 5)

        form = TicketDetailsForm
        
        context = {**get_navbar(),'user': user,
                   'notifications_count': notifications_count,
                   'tickets_replies': tickets_replies,
                   'ticket': ticket,
                   'tickets_admin_replies': tickets_admin_replies,
                   'ticket_is_open': ticket_is_open,
                   'form': form,
                   }
        
        return render(request, 'user_panel_ticket_details.html', context)
    
    def post(self, request, id):
        user,user_id,notifications_count = panel_base_data(request)
        
        form = TicketDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            ticket = Ticket.objects.get(id=id)
            TicketDetails.objects.create(ticket=ticket, user=request.user,
                                         message=cd['message'], file=cd['file'])
            cache.delete(f'tickets_replies-{user_id}')
            messages.success(request, 'تیکت شما  ارسال شد', 'success')
            return redirect('ticket-details', id)
        context = {**get_navbar(),'form': form,
                   'user': user, 
                   'notifications_count': notifications_count}
        
        return render(request, 'user_panel_ticket_details.html', context)
        


class TicketCloseByUserView(View):
    def get(self, request, id):
        user_id = request.session.get('_auth_user_id')
        ticket = get_object_or_404(Ticket, id=id)
        ticket.user_closed = True
        ticket.save()
        cache.delete(f'tickets-{user_id}')
        cache.delete(f'tickets_replies-{user_id}')
        return redirect('ticket-list')



class TicketCreateView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        form = TicketForm
        context = {**get_navbar(),'form': form,
                   'user': user, 
                   'notifications_count': notifications_count}
        return render(request, 'user_panel_create_ticket.html', context)
    
    def post(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            ticket = Ticket.objects.create(user=request.user,
                                  department=cd['department'],
                                  subject=cd['subject'])
            TicketDetails.objects.create(ticket=ticket, user=request.user,
                                         message=cd['message'], file=cd['file'])
            messages.success(request, 'تیکت شما ارسال ساخته شد', 'success')
            cache.delete(f'tickets-{user_id}')
            return redirect('ticket-list')
        context = {**get_navbar(),'form': form,
                   'user': user, 
                   'notifications_count': notifications_count}
        return render(request, 'user_panel_create_ticket.html', context)


class BookmarksView(View):
    def get(self, request):
        user, user_id, notifications_count = panel_base_data(request)
        
        page = request.GET.get('page', '1')
        count = 20
        
        bookmarks = cache.get(f'user-{user_id}-bookmarks')
        paginator = cache.get(f'user-{user_id}-bookmarks-paginator{page}')
        if not bookmarks:
            bookmarks = Bookmark.objects.select_related('movie', 'movie__category').filter(user_id=user_id).annotate(
                count_of_favorite=Count('movie__favorite')).values(
                    'id', 'movie_id', 'movie__name', 'movie__summary',
                    'movie__imdb_rate', 'movie__is_ongoing', 'movie__created_at',
                    'movie__release_at', 'movie__category__id', 'movie__category__title', 'count_of_favorite')
            bookmarks,paginator = get_paginator(request, bookmarks, count)
            cache.set(f'user-{user_id}-bookmarks', bookmarks, 60 * 10)
            cache.set(f'user-{user_id}-bookmarks-paginator{page}', paginator, 60 * 10)
            
        bookmarks_counts = len(bookmarks) * int(page)
        max_bookmarks_counts = paginator.count
        context = {**get_navbar(),
                'user': user, 
                'bookmarks': bookmarks,
                'paginator': paginator,
                'bookmarks_counts': bookmarks_counts,
                'max_bookmarks_counts': max_bookmarks_counts,
                'notifications_count': notifications_count}
        return render(request, 'user_panel_bookmark.html', context)


class FavoriteView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        
        page = request.GET.get('page', '1')
        count = 20
        
        favorites = cache.get(f'user-{user_id}-favorite-{page}')
        paginator = cache.get(f'user-{user_id}-favorite-paginator{page}')
        if not favorites:
            favorites = Favorite.objects.select_related('movie', 'movie__category').filter(user_id=user_id).annotate(
                    count_of_favorite=Count('movie__favorite')).values(
                        'id', 'movie_id', 'movie__name', 'movie__summary',
                        'movie__imdb_rate', 'movie__is_ongoing', 'movie__created_at',
                        'movie__release_at', 'movie__category__id', 'movie__category__title', 'count_of_favorite')
            favorites,paginator = get_paginator(request, favorites, count)
            cache.set(f'user-{user_id}-favorite-{page}', favorites, 60 * 10)
            cache.set(f'user-{user_id}-favorite-paginator{page}', paginator, 60 * 10)
            
        favorites_counts = len(favorites) * int(page)
        max_favorites_counts = paginator.count
        print(favorites_counts)
        context = {**get_navbar(),
                   'user': user, 
                   'favorites': favorites,
                   'favorites_counts': favorites_counts,
                   'max_favorites_counts': max_favorites_counts,
                   'paginator': paginator,
                   'notifications_count': notifications_count}
        return render(request, 'user_panel_favorite.html', context)


class CommentView(View):
    def get(self, request):
        user,user_id,notifications_count = panel_base_data(request)
        
        page = request.GET.get('page', '1')
        count = 20
        
        comments = cache.get(f'user-{user_id}-comments-{page}')
        paginator = cache.get(f'user-{user_id}-comments-paginator{page}')
        if not comments:
            comments = Comment.objects.filter(user_id=user_id).select_related('movie').values(
                'id', 'text', 'created_at','movie__name', 'movie__id',
                                'movie__category__title', 'movie__name',
                                'like', 'dislike')
            comments,paginator = get_paginator(request, comments, count)
            cache.set(f'user-{user_id}-comments-{page}', comments, 60 * 10)
            cache.set(f'user-{user_id}-comments-paginator{page}', paginator, 60 * 10)
        comments_id = [comment['id'] for comment in comments]
        
        replies = cache.get(f'user-{user_id}-replies')
        if not replies:
            replies = Reply.objects.filter(reply_to__id__in=comments_id).values('reply_to',
                'id', 'created_at', 'user__username', 'text', 'like', 'dislike')
            cache.set(f'user-{user_id}-replies', replies, 60 * 10)
            
        comments_counts = len(comments) * int(page)
        max_comments_counts = paginator.count
        
        context = {**get_navbar(),
                'user': user,
                'max_comments_counts': max_comments_counts,
                'comments_counts': comments_counts,
                'comments': comments,
                'replies': replies,
                'paginator': paginator,
                'notifications_count': notifications_count}
        
        return render(request, 'user_panel_comments.html', context)