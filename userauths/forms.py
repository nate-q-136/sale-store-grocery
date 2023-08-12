from django import forms 
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    # set for username: input[type="text"]
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    # set for email: input[type=email"]
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    # set for password: input[type=password"]
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username', 'email']
    pass