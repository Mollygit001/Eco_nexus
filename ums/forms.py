from django import forms
from .models import Enrollment, GradeSubmission


class EnrollmentForm(forms.ModelForm):
    """
    Form for student course enrollment
    """
    class Meta:
        model = Enrollment
        fields = []  # No fields to display - enrollment is based on student + course
    
    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        self.course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        """
        Override save to set student and course
        """
        enrollment = super().save(commit=False)
        if self.student:
            enrollment.student = self.student
        if self.course:
            enrollment.course = self.course
        
        if commit:
            enrollment.save()
        return enrollment


class GradeSubmissionForm(forms.ModelForm):
    """
    Form for instructors to submit/update student grades
    """
    class Meta:
        model = GradeSubmission
        fields = ['grade']
        widgets = {
            'grade': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course', None)
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        """
        Override save to set course and student
        """
        grade = super().save(commit=False)
        if self.course:
            grade.course = self.course
        if self.student:
            grade.student = self.student
        
        if commit:
            grade.save()
        return grade


class CourseFilterForm(forms.Form):
    """
    Form for filtering courses
    """
    GRADE_CHOICES = [
        ('', 'All Courses'),
    ]
    
    search = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by course code or title...',
        })
    )
    
    department = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Department',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Import here to avoid circular imports
        from .models import Department
        self.fields['department'].queryset = Department.objects.all()
