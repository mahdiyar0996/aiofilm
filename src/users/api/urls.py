from django.contrib import admin
from django.urls import path, include
from .views import ActivateCodeView, UserActivateView, ResetPasswordTokenView

urlpatterns = [
    path('send-activate-code/<int:pk>/', ActivateCodeView.as_view(), name='send-activate-code'),
    path('user-activate/<str:uidb64>/<str:token>/', UserActivateView.as_view(), name='user-activate'),
    path('password-recovery-token/', ResetPasswordTokenView.as_view(), name='password-recovery-token'),
]