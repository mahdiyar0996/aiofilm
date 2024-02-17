from django.core.validators import ValidationError, RegexValidator, MinLengthValidator


def valid_email():
    validator = RegexValidator('^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$',
                               message='ایمیل وارد شده معتبر نمی باشد',
                               code='invalid')
    return validator


def valid_username():
    validator = RegexValidator('([a-zA-Z0-9_]+)',
                   message='نام کاربری باید از حروف اعداد و ـ باشد', code='invalid')

    return validator


def valid_password():
    validator = RegexValidator("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", code='valid',
                   message='')
    return validator
