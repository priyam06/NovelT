from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:

        model = User


        fields = [
                    'username',
                    'email',
                    'password1',
                    'password2',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = [
                    'age',
                    'location',
                    'occupation',
                    'bio',
                    'profile_pic',
        ]



class UserUpdateForm(forms.ModelForm):


    class Meta:
        model = User

        fields = [
                    'username',
                    'email',
                    'first_name',
                    'last_name',
        ]

        help_texts = {
            'username': None,
        }
