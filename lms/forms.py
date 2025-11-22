from django import forms
from django.forms import ModelForm
from .models import Quiz, Attempt, GamificationLedger


class QuizAttemptForm(forms.Form):
    """
    Dynamic quiz submission form
    Generated at runtime based on quiz questions
    """
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        
        # Add a field for each question
        for question in quiz.questions.all():
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.text,
                required=False
            )


class QuizFilterForm(forms.Form):
    """
    Filter quizzes by difficulty or topic
    """
    DIFFICULTY_CHOICES = [
        ('', 'All Difficulties'),
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md',
            'placeholder': 'Search quizzes...'
        })
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )


class LessonContentForm(forms.Form):
    """
    Mark lesson as completed / track progress
    """
    content_id = forms.IntegerField(widget=forms.HiddenInput())
    completed = forms.BooleanField(required=False)


class GamificationReportForm(forms.Form):
    """
    Filter gamification entries for reporting
    """
    EVENT_CHOICES = [
        ('', 'All Events'),
        ('quiz_completed', 'Quiz Completed'),
        ('badge_earned', 'Badge Earned'),
        ('module_completed', 'Module Completed'),
    ]
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )
    
    event = forms.ChoiceField(
        choices=EVENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md'
        })
    )
