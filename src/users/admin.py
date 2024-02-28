from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin
from .models import (User, Groups,Favorite,
                     Bookmark, Comment, Reply,
                     Ticket, TicketAdminReply, Notification,
                     TicketDetails)
import nested_admin

class FavoriteAdmin(admin.StackedInline):
    model = Favorite
    extra = 0
    fields = ['movie', 'user']

class BookmarkAdmin(admin.StackedInline):
    model = Bookmark
    fields = ['movie', 'user']
    extra = 0

admin.site.unregister(Group)
@admin.register(Groups)
class GroupAdmin(GroupAdmin):
    fields = ['name', 'permissions']
    list_display = ['name']
    list_display_links = ['name']
    list_filter = ['name',]
    search_fields = ['name']
    
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # fields = '__all__'
    fieldsets = (
        # ("Permissions",{"fields": ("groups","user_permissions",),},),
        ('', {'fields': ['username', 'email', "avatar",'password', 'ipaddress']}),
        ('', {'fields': ['first_name', 'last_name', 'city', 'age', 'sex']}),
        ('', {'fields': ['is_superuser', 'is_staff', 'is_active', 'subscribe']}),
        ('', {'fields': ['created_at', 'updated_at', 'last_password_reset']})
    )
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    list_display_links = ['id', 'username', 'email']
    list_per_page = 100
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    search_fields = ['id', 'username', 'email']
    readonly_fields = ['created_at', 'updated_at', 'last_password_reset']
    inlines = [FavoriteAdmin, BookmarkAdmin]

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ['user', 'movie', 'text', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'user', 'movie', 'is_active']
    list_display_links = ['id', 'user', 'movie']
    list_per_page = 100
    list_filter = ['is_active',]
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    fields = ['user','reply_to', 'movie', 'text','like', 'dislike', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'user', 'reply_to', 'movie', 'is_active']
    list_display_links = ['id', 'user', 'reply_to', 'movie']
    list_per_page = 100
    list_filter = ['is_active',]
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    
    
class TicketAdminReplyAdmin(nested_admin.NestedStackedInline):
    model = TicketAdminReply
    fields = ['user','ticket','message', 'file', 'created_at', 'updated_at']
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    # prepopulated_fields = {'message': ('ticket', )}

class TicketDetailsAdmin(nested_admin.NestedStackedInline):
    model = TicketDetails
    fields = ['ticket','user','message', 'file','created_at', 'updated_at']
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TicketAdminReplyAdmin,]


@admin.register(Ticket)
class TicketAdmin(nested_admin.NestedModelAdmin):
    fields = ['user','department','subject', 'admin_closed', 'user_closed', 'created_at', 'updated_at']
    list_display = ['id', 'department', 'user', 'subject', 'admin_closed', 'user_closed', 'created_at', 'updated_at']
    list_display_links = ['id', 'department', 'user', 'subject']
    list_per_page = 100
    list_filter = ['admin_closed', 'user_closed']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TicketDetailsAdmin,]


@admin.register(TicketAdminReply)
class TicketReplyAdmin(admin.ModelAdmin):
    fields = ['ticket','user','message', 'file', 'created_at', 'updated_at']
    list_display = ['id','message', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'message']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = ['subject', 'message', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'subject', 'message', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'subject']
    readonly_fields = ['created_at', 'updated_at']