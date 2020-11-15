from django import forms
from .models import Customer
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
import re
from .validators import match_password
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm, UserChangeForm

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10,min_length=10,strip=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password1','password2']
        widgets = {
            'last_name':forms.TextInput(attrs={'placeholder':'Optional field can be left blank'})
        }


    def clean_first_name(self):
        value = self.cleaned_data.get('first_name')
        if value.strip()=='':
            raise ValidationError('This field is required')
        pattern = r'[a-zA-Z ]+'
        if re.fullmatch(pattern,value):
            return value
        else:
            raise ValidationError('Only alphabets are allowed')

    def clean_email(self):
        value = self.cleaned_data.get('email')
        obj = Customer.objects.filter(email=value)
        if obj.exists():
            raise forms.ValidationError('User with this email already exists')
        else:
            return value

    def clean_mobile(self):
        value = self.cleaned_data.get('mobile')
        obj = Customer.objects.filter(mobile=value)
        pattern=r'[\d]{10}'
        if obj.exists():
            raise forms.ValidationError('User with this mobile number already exists')
        elif not re.fullmatch(pattern,value):
            raise ValidationError('Enter valid mobile number')
        else:
            return value



class ForgotPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'


#
# class ForgotPasswordForm(PasswordResetForm):
#     class Meta:
#         model = User
#         fields = '__all__'


class UserProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name','last_name','email','last_login','date_joined']
