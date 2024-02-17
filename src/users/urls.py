from django.contrib import admin
from django.urls import path, include
from .views import (LoginView, RegisterView,
ResetPasswordView, ResetPasswordCompleteView,
PanelView, LogoutView, PanelChangePasswordView,
PanelEditAccountView)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('password-recovery', ResetPasswordView.as_view(), name='password-recovery'),
    path('password-recovery-complete/<str:uidb64>/<str:token>', ResetPasswordCompleteView.as_view(), name='password-recovery-complete'),
    path('panel', PanelView.as_view(), name='user-panel'),
    path('panel/change-password', PanelChangePasswordView.as_view(), name='change-password'),
    path('panel/edit-account', PanelEditAccountView.as_view(), name='user-edit-account'),
    path('', include('users.api.urls')),
]