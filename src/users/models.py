from django.db import models
from django.db.models import F, Q, Count
from django.contrib.auth.models import (BaseUserManager, Group as DjangoGroup,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from django_jalali.db import models as jmodels
from .validators import valid_username, valid_email, valid_password
from config.settings import redis
import json
import time

class AbstractBase(models.Model):
    updated_at = jmodels.jDateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = jmodels.jDateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True)
    
    def active_users(self):
        return self.objects.filter(is_active=True)
    
    class Meta:
        abstract = True

class Groups(DjangoGroup):
    
    class Meta:
        db_table = 'Groups'
        verbose_name = 'group'
        verbose_name_plural = 'groups'
        proxy = True
        

  
        
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, email, password, is_superuser, is_staff, is_active, **kwargs):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password,
                    is_superuser=False, is_staff=False, is_active=False, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)
    def create_superuser(self, username, email, password,
                         is_superuser=True, is_staff=True, is_active=True, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)
        
class User(AbstractBaseUser, PermissionsMixin, AbstractBase):
    objects = UserManager()
    username = models.CharField('نام کاربری', max_length=64, unique=True, validators=[valid_username()],
                                error_messages={'unique': 'کاربری با این نام وجود دارد',
                                                'invalid': 'نام کاربری باید از حروف,اعداد و ـ باشد'})
    email = models.EmailField('ایمیل' ,max_length=64, unique=True, validators=[valid_email()],
                              error_messages={'unique': 'کاربری با این ایمیل وجود دارد',
                                              'invalid': 'لطفا یک ایمیل معتبر وارد کنید'})
    password = models.CharField('رمز عبور', max_length=254,
                                error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ  و یک عدد داشته باشد'})
    last_password_reset = jmodels.jDateField("زمان آخرین تغییر رمزعبور",null=True, blank=True)
    first_name = models.CharField('نام', max_length=64, blank=True, null=True)
    last_name = models.CharField('نام خانوادگی', max_length=64, blank=True, null=True)
    city = models.CharField('شهر', max_length=55, blank=True, null=True)
    age = models.SmallIntegerField('سن', blank=True, null=True)
    sex = models.CharField('جنسیت', max_length=55, blank=True, null=True)
    is_superuser = models.BooleanField('ادمین', db_default=False, db_index=True)
    is_staff = models.BooleanField('کارکنان', db_default=False, db_index=True)
    is_active = models.BooleanField("وضعیت", default=False)
    subscribe = models.DateTimeField('زمان اشتراک', blank=True, null=True)
    ipaddress = models.GenericIPAddressField('ایپی آدرس', blank=True, null=True)
    avatar = models.ImageField('آواتار', default='users/default.jpg', upload_to='users/', blank=True, )
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']
    
    
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['created_at']
        
    def __str__(self):
        return self.username
    
    
    def staff_users(self):
        return self.objects.filter(is_staff=True)

    def admin_users(self):
        return self.objects.filter(is_admin=True)
    
    def to_dict(self):
        return {
        'id': self.id or '',
        'pk': self.pk or '',
        "username" : self.username or '',
        'subscribe': str(self.subscribe) or '',
        "email" : self.email or '',
        "last_password_reset" : self.last_password_reset or '',
        "first_name" : self.first_name or '',
        "last_name" : self.last_name or '',
        "city" : self.city or '',
        "age" : self.age or '',
        'sex': self.sex or '',
        "ipaddress" : self.ipaddress or '',
        "avatar" : str(self.avatar) or '',}
        
    def get_current_user(request, field=None):
        user_id = request.session.get('_auth_user_id')
        if not field:
            user = redis.hgetall(f"user-{user_id}")
            if not user and user_id:
                user = request.user.to_dict()
                with redis.pipeline() as pipeline:
                    pipeline.hset(f"user-{user_id}", mapping=request.user.to_dict())
                    pipeline.expire(f"user-{user_id}", 60 * 30)
                    pipeline.execute()
            user['avatar'] = request.build_absolute_uri('/media/' + user['avatar'])
        else:
            user = redis.hget(f"user-{user_id}", field)
            if not user and user_id:
                try:
                    user = request.user.to_dict()
                    with redis.pipeline() as pipeline:
                        pipeline.hset(f"user-{user_id}", mapping=request.user.to_dict())
                        pipeline.expire(f"user-{user_id}", 60 * 30)
                        pipeline.execute()
                    user = user[field]
                except AttributeError:
                    return None
        return user
    
    
class Favorite(AbstractBase):
    movie = models.ForeignKey('products.Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    is_active = None
    class Meta:
        db_table = 'Favorite'
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
    
    def __str__(self):
        return self.movie.name
    
class Bookmark(AbstractBase):
    movie = models.ForeignKey('products.Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    is_active = None
    class Meta:
        db_table = 'Bookmark'
        verbose_name = 'bookmark'
        verbose_name_plural = 'bookmarks'
    
    def __str__(self):
        return self.movie.name    

class Comment(AbstractBase):
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    movie = models.ForeignKey('products.Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE)
    text = models.TextField('متن')
    like = models.IntegerField('لایک', default=0)
    dislike = models.IntegerField('دیس لایک', default=False)
    updated_at = models.DateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = models.DateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True)
    
    class Meta:
        db_table = 'Comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    
    def __str__(self):
        return self.user.username

class Reply(AbstractBase):
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    reply_to = models.ForeignKey(Comment, verbose_name='پاسخ به', related_name='reply_to', on_delete=models.CASCADE)
    movie = models.ForeignKey('products.Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE)
    text = models.TextField('متن')
    like = models.IntegerField('لایک', default=0)
    dislike = models.IntegerField('دیس لایک', default=0)
    updated_at = models.DateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = models.DateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True)

    class Meta:
        db_table = 'Reply'
        verbose_name = 'reply'
        verbose_name_plural = 'replies'
        ordering = ['created_at']
    
    def __str__(self):
        return self.user.username



class Ticket(AbstractBase):
    departments = (
        ('پشتیبانی', 'پشتیبانی'),
        ('مشکلات فنی', 'مشکلات فنی'),
        ('پیشنهادات و انتقادات', 'پیشنهادات و انتقادات'),
        ('اپلیکیشن', 'اپلیکیشن'),
        ('مشکلات ترجمه', 'مشکلات ترجمه'),
    )
    
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    department = models.CharField('دپارتمان', choices=departments, max_length=64, db_index=True)
    subject = models.CharField('موضوغ', max_length=252)
    is_active = None
    admin_closed = models.BooleanField('بسته شده توسط ادمین', default=False)
    user_closed = models.BooleanField('بسته شده توسط کاربر', default=False)
    created_at = models.DateTimeField("زمان ساخت",auto_now_add=True)
    
    class Meta:
        db_table = 'Ticket'
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
    
    def __str__(self):
        return self.user.username
    
class TicketDetails(AbstractBase):
    ticket = models.ForeignKey(Ticket, verbose_name='تیکت', related_name='%(class)s', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    message = models.TextField('پیغام')
    file = models.FileField("فایل", blank=True, null=True, upload_to='files/ticket/')
    updated_at = models.DateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = models.DateTimeField("زمان ساخت",auto_now_add=True)
    
    class Meta:
        db_table = 'TicketDetails'
        verbose_name = 'ticket_detail'
        verbose_name_plural = 'ticket_details'
    
    def __str__(self):
        return self.ticket.subject
    
class TicketAdminReply(AbstractBase):
    ticket = models.ForeignKey(TicketDetails, verbose_name='تیکت', related_name='%(class)s', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    message = models.TextField('پیغام')
    file = models.FileField("فایل", blank=True, null=True, upload_to='files/ticket_replies/')
    updated_at = models.DateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = models.DateTimeField("زمان ساخت",auto_now_add=True)
    
    class Meta:
        db_table = 'Ticket_Reply'
        verbose_name = 'ticket_reply'
        verbose_name_plural = 'ticket_replies'
    
    def __str__(self):
        return self.user.username
    
class Notification(AbstractBase):
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.DO_NOTHING, blank=True, null=True)
    subject =  models.CharField('موضوع',max_length=255,)
    message = models.TextField('پیغام',)
    is_read = models.BooleanField('خوانده شده',default=False, blank=True)
    class Meta:
        db_table = 'Notification'
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
    
    def __str__(self):
        return self.subject
    
    
    
    def get_user_notifications_count(user_id):
        notifications_count = redis.hgetall(f'notification-{user_id}')
        if not notifications_count:
            notifications_count = Notification.objects.filter(Q(is_read=False) & Q (user__id=user_id) | Q(user__id=None)).aggregate(count=Count('id'))
            with redis.pipeline() as pipeline:
                pipeline.hset(f'notification-{user_id}', 'count', str(notifications_count['count']))
                pipeline.expire(f'notification-{user_id}', 60 * 10)
                pipeline.execute()
        return notifications_count
    
    