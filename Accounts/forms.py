from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
from datetime import datetime


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username',
               }))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',

        }
    ))


class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)
        help_texts = {'username': None}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords are not the same.")
        return cd['password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'firstname', 'lastname', 'gender', 'date_of_birth', 'phone', 
            'city', 'country', 'profile_picture', 'motto', 'bio']
        widgets = {
            'date_of_birth': forms.SelectDateWidget(
                years=range(1900, datetime.now().year + 1)),
        }
