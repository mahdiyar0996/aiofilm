from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegisterView, ResetPasswordView, ResetPasswordCompleteView, UserPanelView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('password-recovery', ResetPasswordView.as_view(), name='password-recovery'),
    path('password-recovery-complete/<str:uidb64>/<str:token>', ResetPasswordCompleteView.as_view(), name='password-recovery-complete'),
    path('panel', UserPanelView.as_view(), name='user-panel'),
    path('', include('users.api.urls')),
]