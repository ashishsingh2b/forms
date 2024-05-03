from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class SignupForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)
    class Meta:
        model =User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}

class EditUserForm(UserChangeForm):
    password = None
    class Meta:
        model =User
        fields ='__all__'
        fields =['username','first_name','last_name','email','date_joined','last_login']
        labels = {'email':'Email'}


class EditAdminForm(UserChangeForm):
    password = None
    class Meta:
        model =User
        fields ='__all__'
        labels = {'email':'Email'}
