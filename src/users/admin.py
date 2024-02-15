from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin
from .models import User, Groups,Favorite, Bookmark, Comment, Reply, Ticket, TicketReply, Notification

class FavoriteAdmin(admin.StackedInline):
    model = Favorite
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
    fieldsets = (
        ("Permissions",{"fields": ("groups","user_permissions",),},),
        ('', {'fields': ['username', 'email', "avatar",'password', 'ipaddress']}),
        ('', {'fields': ['first_name', 'last_name', 'city', 'age']}),
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
    fields = ['user','reply_to', 'movie', 'text', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'user', 'reply_to', 'movie', 'is_active']
    list_display_links = ['id', 'user', 'reply_to', 'movie']
    list_per_page = 100
    list_filter = ['is_active',]
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    
    
class TicketReplyAdmin(admin.StackedInline):
    model = TicketReply
    fields = ['ticket', 'message', 'file', 'created_at', 'updated_at']
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    fields = ['user','department','subject', 'message', 'file', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'department', 'user', 'subject', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'department', 'user', 'subject']
    list_per_page = 100
    list_filter = ['is_active',]
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    # readonly_fields = ['user', 'department', 'subject', 'message', 'file', 'created_at', 'updated_at']
    inlines = [TicketReplyAdmin,]


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    fields = ['ticket', 'message', 'file', 'created_at', 'updated_at']
    list_display = ['id', 'ticket', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'ticket']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Notification)
class TicketReplyAdmin(admin.ModelAdmin):
    fields = ['subject', 'message', 'is_active', 'created_at', 'updated_at']
    list_display = ['id', 'subject', 'message', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'subject']
    readonly_fields = ['created_at', 'updated_at']