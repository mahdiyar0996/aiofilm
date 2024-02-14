from rest_framework.views import APIView, Response
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from ..models import User
from ..tokens import email_verification_token
from .serializers import ResetPasswordSerializer
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from threading import Thread

class ActivateCodeView(APIView):
    def get(self, request, pk):
        current_site = get_current_site(request)
        
        user = User.objects.get(pk=pk)
        
        message = render_to_string('activate_code.html', {
        'user': user,
        'domain': current_site.domain,
        'scheme': request.scheme,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    })
        headers = {'Importance': 'important'}
        email = EmailMessage(subject='فعال سازی حساب کاربری', body=message, to=[user.email,], headers=headers)
        th1 = Thread(target=email.send)
        th1.start()
    
        return Response(status=status.HTTP_200_OK)
        
        

class UserActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'حساب شما با موفقیت فعال شد')
            return redirect('login')
        else:
            messages.error(request, 'لینک فعال سازی نامعتبر است')
            return redirect('login')


class ResetPasswordTokenView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            try:
                current_site = get_current_site(request)
                user = User.objects.get(email=request.data.get('email'))
                
                message = render_to_string('password_recovery.html', {
                'user': user,
                'domain': current_site.domain,
                'scheme': request.scheme,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            })
                headers = {'Importance': 'important'}
                email = EmailMessage(subject='بازیابی رمزعبور', body=message, to=[user.email,], headers=headers)
                th1 = Thread(target=email.send)
                th1.start()
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد", 'danger')
        return Response(status=status.HTTP_400_BAD_REQUEST)