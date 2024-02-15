from django.contrib import admin
from .models import Subscribe, Payment, PaymentMethod


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'discount', 'time', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'name', 'price', 'discount', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_active',]
    readonly_fields = ['created_at', 'updated_at']
    

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    fields = ['user', 'subscribe', 'method']
    list_display = ['id', 'user', 'subscribe', 'method']
    list_display_links = ['id', 'user', 'subscribe', 'method']
    list_filter = ['subscribe', 'method']
    search_fields = ['user',]
    readonly_fields = ['created_at', 'updated_at']
    

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    fields = ['name', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'name', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['name',]
    search_fields = ['name',]
    readonly_fields = ['created_at', 'updated_at']

