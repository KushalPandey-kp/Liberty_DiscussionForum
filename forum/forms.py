from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Discussion, Reply
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

import re

class SignupForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    role = forms.ChoiceField(label="Role", choices=UserProfile.ROLE_CHOICES)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalpha():
            raise forms.ValidationError("Username must contain only letters (a-z).")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@libertycollege.edu.np'):
            raise forms.ValidationError("Only libertycollege.edu.np emails are allowed.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and len(password1) < 6:
            self.add_error('password1', "Password must be at least 6 characters long.")
        if password1 != password2:
            self.add_error('password2', "Passwords do not match.")
    
    def save(self):
        # Create the user
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        # Create the user profile with role
        UserProfile.objects.create(
            user=user,
            role=self.cleaned_data['role']
        )
        return user

   


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title','content','image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500',
                'rows': 5
            })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']