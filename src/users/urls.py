from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegisterView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
]