from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('department', 'semester')
        widgets = {
            'department': forms.Select(attrs={'class': 'block w-full rounded-md border-gray-300'}),
            'semester': forms.Select(attrs={'class': 'block w-full rounded-md border-gray-300'}),
        }
