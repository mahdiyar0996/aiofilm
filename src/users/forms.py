from django import forms
from .models import User
from string import digits
import re
from django.db.models import Q

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, required=True, label='نام کاربری',)
    password = forms.CharField(required=True, label='گذرواژه')
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if password != password.lower and re.search('\d', password):
            return password
        else:
            raise forms.ValidationError('نام کاربری یا گذرواژه اشتباه است', 'invalid')


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(min_length=8, max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد'
    })
    password2 = forms.CharField(min_length=8, max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور مطابقت ندارد'
    })
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    
    def clean(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        re.search('\d', password1)
        if not re.search('\d', password1):
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
    password1 = forms.CharField(min_length=8, max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد'
    })
    password2 = forms.CharField(min_length=8, max_length=55, required=True, error_messages={
        'invalid': 'رمز عبور مطابقت ندارد'
    })
    
    def clean(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        re.search('\d', password1)
        if not re.search('\d', password1):
            self.add_error('password1', 'رمز عبور باید حداقل ۸ کاراکتر و یک حرف بزرگ و یک عدد داشته باشد')
        elif password2 != password1:
            self.add_error('password2', 'رمز عبور مطابقت ندارد')
        return cd