from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import (BaseUserManager, Group as DjangoGroup,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from django_jalali.db import models as jmodels
from .validators import valid_username, valid_email, valid_password


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
    password = models.CharField('رمز عبور', max_length=254, validators=[valid_password()],
                                error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ  و یک عدد داشته باشد'})
    last_password_reset = models.DateTimeField("زمان آخرین تغییر رمزعبور",null=True, blank=True)
    first_name = models.CharField('نام', max_length=64, blank=True, null=True)
    last_name = models.CharField('نام خانوادگی', max_length=64, blank=True, null=True)
    city = models.CharField('شهر', max_length=55, blank=True, null=True)
    age = models.SmallIntegerField('سن', blank=True, null=True)
    is_superuser = models.BooleanField('ادمین', db_default=False, db_index=True)
    is_staff = models.BooleanField('کارکنان', db_default=False, db_index=True)
    is_active = models.BooleanField("وضعیت", default=False)
    ipaddress = models.GenericIPAddressField('ایپی آدرس', blank=True, null=True)
    avatar = models.ImageField('آواتار', default='/media/users/default.jpg', upload_to='media/users/', blank=True, )
    objects = UserManager()
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
        "username" : self.username or '',
        "email" : self.email or '',
        "last_password_reset" : self.last_password_reset or '',
        "first_name" : self.first_name or '',
        "last_name" : self.last_name or '',
        "city" : self.city or '',
        "age" : self.age or '',
        "ipaddress" : self.ipaddress or '',
        "avatar" : str(self.avatar) or '',}
    
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
    
    class Meta:
        db_table = 'Comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    
    def __str__(self):
        return self.user.username

class Reply(AbstractBase):
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, verbose_name='پاسخ به', related_name='reply_to', on_delete=models.CASCADE)
    movie = models.ForeignKey('products.Movie', verbose_name='فیلم', related_name='%(class)s', on_delete=models.CASCADE)
    text = models.TextField('متن')

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
    message = models.TextField('پیغام')
    file = models.FileField("فایل", blank=True, null=True, upload_to='files/ticket/')
    
    class Meta:
        db_table = 'Ticket'
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
    
    def __str__(self):
        return self.user.username
    
    
    
class TicketReply(AbstractBase):
    ticket = models.ForeignKey(Ticket, verbose_name='تیکت', related_name='%(class)s', on_delete=models.CASCADE)
    message = models.TextField('پیغام')
    file = models.FileField("فایل", blank=True, null=True, upload_to='files/ticket_replies/')
    
    class Meta:
        db_table = 'Ticket_Reply'
        verbose_name = 'ticket_reply'
        verbose_name_plural = 'ticket_replies'
    
    def __str__(self):
        return self.user.username