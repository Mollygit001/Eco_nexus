from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('ums.Department', on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey('ums.Semester', on_delete=models.SET_NULL, null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sustainability_score = models.PositiveIntegerField(default=0)
    skills = models.JSONField(default=list, blank=True)
    badges = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"


@receiver(post_save, sender=User)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    # Only create for non-staff users by default; can be adjusted later
    if created and not instance.is_staff:
        StudentProfile.objects.create(user=instance, student_id=f"S{instance.id:06d}")
    else:
        if hasattr(instance, 'student_profile'):
            instance.student_profile.save()
