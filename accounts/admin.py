from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_id", "department", "semester", "gpa", "sustainability_score")
    search_fields = ("student_id", "user__username", "user__first_name", "user__last_name")
    list_filter = ("department", "semester")
