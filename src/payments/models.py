from django.db import models
from django.db.models import F, Q
from django_jalali.db import models as jmodels


class AbstractBase(models.Model):
    updated_at = jmodels.jDateTimeField("اخرین بروزرسانی",auto_now=True)
    created_at = jmodels.jDateTimeField("زمان ساخت",auto_now_add=True)
    is_active = models.BooleanField("وضعیت", default=True)
    
    def active_users(self):
        return self.objects.filter(is_active=True)
    class Meta:
        abstract = True


class Subscribe(AbstractBase):
    name = models.CharField('نام اشتراک', max_length=64)
    price = models.IntegerField('قیمت')
    discount = models.SmallIntegerField('تخفیف')
    time = models.SmallIntegerField('زمان (روز)')
    
    class Meta:
        db_table = 'Subscribe'
        verbose_name = 'subscribe'
        verbose_name_plural = 'subscribes'
    
    def __str__(self):
        return self.name

class PaymentMethod(AbstractBase):
    name = models.CharField('نام بانک', max_length=64)

    class Meta:
        db_table = 'Payment_Methods'
        verbose_name = 'payment_methods'
        verbose_name_plural = 'payment_methods'
        
    def __str__(self):
        return self.name
        
        
class Payment(AbstractBase):
    user = models.ForeignKey('users.User', verbose_name='کاربر', related_name="%(class)s", on_delete=models.DO_NOTHING)
    subscribe = models.ForeignKey(Subscribe, verbose_name='اشتراک', related_name='%(class)s', on_delete=models.DO_NOTHING)
    price = models.BigIntegerField('قیمیت')
    method = models.ForeignKey(PaymentMethod, verbose_name='بانک', related_name='%(class)s', on_delete=models.DO_NOTHING)
    is_active = None

    class Meta:
        db_table = 'Payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        
    def __str__(self):
        return self.user.username