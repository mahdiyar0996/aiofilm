from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,)
from django_jalali.db import models as jmodels

class AbstractBase(models.Model):
    updated_at = jmodels.jDateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = jmodels.jDateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True, db_index=True)
    
    def active_users(self):
        return self.objects.filter(is_active=True)
    class Meta:
        abstract = True
        
        
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
                    is_superuser=False, is_staff=False, is_active=True, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)
    def create_superuser(self, username, email, password,
                         is_superuser=True, is_staff=True, is_active=True, **kwargs):
        return self._create_user(username, email, password, is_superuser=is_superuser,
                                 is_staff=is_staff, is_active=is_active, **kwargs)
        
class User(AbstractBaseUser, PermissionsMixin, AbstractBase):
    objects = UserManager()
    username = models.CharField('نام کاربری', max_length=64, unique=True, 
                                error_messages={'unique': 'کاربری با این نام وجود دارد',
                                                'invalid': 'نام کاربری باید از حروف,اعداد و ـ باشد'})
    email = models.EmailField('ایمیل' ,max_length=64, unique=True,
                              error_messages={'unique': 'کاربری با این ایمیل وجود دارد',
                                              'invalid': 'لطفا یک ایمیل معتبر وارد کنید'})
    password = models.CharField('رمز عبور', max_length=254,
                                error_messages={'invalid': 'رمز کاربری باید ۸ کاراکتر یا بیشتر باشد و یک حرف بزرگ  و یک عدد داشته باشد'})
    last_password_reset = models.DateTimeField("زمان آخرین تغییر رمزعبور",null=True, blank=True)
    first_name = models.CharField('نام', max_length=64, blank=True, null=True)
    last_name = models.CharField('نام خانوادگی', max_length=64, blank=True, null=True)
    city = models.CharField('شهر', max_length=55, blank=True, null=True)
    is_superuser = models.BooleanField('ادمین', db_default=False, db_index=True)
    is_staff = models.BooleanField('کارکنان', db_default=False, db_index=True)
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
    
    






class Ticket(AbstractBase):
    user = models.ForeignKey(User, verbose_name='کاربر', related_name='%(class)s', on_delete=models.CASCADE)
    subject = models.CharField('موضوغ', max_length=252)
    message = models.TextField('پیغام')
    file = models.FileField("فایل", blank=True, null=True, upload_to='files/ticket/')
    
    class Meta:
        db_table = 'ticket'
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'
    
    def __str__(self):
        return self.user.username