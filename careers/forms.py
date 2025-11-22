from django import forms
from django.forms import ModelForm
from .models import JobPosting, Application


class ApplicationForm(ModelForm):
    """
    Form for job application submission
    """
    cover_letter = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 5,
            'placeholder': 'Tell the employer why you are interested in this position...'
        }),
        required=False
    )
    
    class Meta:
        model = Application
        fields = ['cover_letter']


class JobPostingForm(ModelForm):
    """
    Form for employers to post job opportunities
    """
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 8,
            'placeholder': 'Describe the job responsibilities and requirements...'
        })
    )
    
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 5,
            'placeholder': 'List the required qualifications and skills...'
        }),
        required=False
    )
    
    class Meta:
        model = JobPosting
        fields = ['title', 'role', 'location', 'salary', 'category', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Job Title'
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Role'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Job Location'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Salary'
            }),
            'category': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Category'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
                'rows': 8,
                'placeholder': 'Describe the job responsibilities and requirements...'
            }),
        }


class JobFilterForm(forms.Form):
    """
    Form for filtering job listings
    """
    JOB_TYPE_CHOICES = [
        ('', 'All Job Types'),
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Search jobs, companies...'
        })
    )
    
    job_type = forms.ChoiceField(
        choices=JOB_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    
    min_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Min Salary'
        })
    )
    
    max_salary = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Max Salary'
        })
    )


class UpdateApplicationStatusForm(forms.Form):
    """
    Form for employers to update application status
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('interviewed', 'Interviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md',
            'rows': 3,
            'placeholder': 'Add notes for this status change (optional)...'
        }),
        required=False
    )
