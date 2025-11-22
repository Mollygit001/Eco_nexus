from django.db import models
from django.contrib.auth.models import User


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name


class JobPosting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"


class GreenProfile(models.Model):
    student = models.OneToOneField('accounts.StudentProfile', on_delete=models.CASCADE, related_name='green_profile')
    sustainability_score = models.PositiveIntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"GreenProfile: {self.student.student_id}"


class Application(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', blank=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'student')

    def __str__(self):
        return f"{self.student.student_id} -> {self.job.title}"


# Added EmployerProfile model
class EmployerProfile(models.Model):
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    logo = models.ImageField(upload_to='employer_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.employer.company_name}"
