from django.contrib.auth.forms import AuthenticationForm
from django import forms

class StudentAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-200'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-200'}))
