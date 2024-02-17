from django import forms
from .models import User
from string import digits
import re
from django.db.models import Q
from .validators import valid_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, required=True, label='نام کاربری',)
    password = forms.CharField(required=True, label='گذرواژه')
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
            return password
        else:
            raise forms.ValidationError('نام کاربری یا گذرواژه اشتباه است', 'invalid')


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد'
    })
    password2 = forms.CharField(max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور مطابقت ندارد'
    })
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    
    def clean(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password1):
            self.add_error('password1', 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد')
        elif password2 != password1:
            self.add_error('password2', 'رمز عبور مطابقت ندارد')
        return cd
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if user:
                raise forms.ValidationError('کاربری با این نام کاربری وجود دارد')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user:
                raise forms.ValidationError('کاربری با این ایمیل وجود دارد')
        except User.DoesNotExist:
            return email


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=128, required=True, error_messages={
        'invalid': 'لطفا یک ایمیل معتبر وارد کنید'
    })
    

class ResetPasswordCompleteForm(forms.Form):
    password1 = forms.CharField(max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد'
    })
    password2 = forms.CharField(max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور مطابقت ندارد'
    })
    
    def clean(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password1):
            self.add_error('password1', 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد')
        elif password2 != password1:
            self.add_error('password2', 'رمز عبور مطابقت ندارد')
        return cd




class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=55, required=True)
    password1 = forms.CharField( max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد'
    })
    password2 = forms.CharField(max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور مطابقت ندارد'
    })
    
    def clean(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password1):
            self.add_error('password1', 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد')
        elif password2 != password1:
            self.add_error('password2', 'رمز عبور مطابقت ندارد')
        return cd


class ChangeUserInformationForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=False)
    genders = (
        (None, 'جنسیت خود را نتخاب کنید'),
        (1, 'مرد'),
        (2, 'زن'),
    )
    sex = forms.ChoiceField(choices=genders)
    avatar = forms.ImageField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'city', 'age', 'sex', 'avatar']