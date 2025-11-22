from django.contrib import admin
from .models import Department, Semester, Course, Enrollment, GradeSubmission

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    list_filter = ("start_date", "end_date")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "semester", "credits", "instructor")
    search_fields = ("code", "title")
    list_filter = ("department", "semester")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_on")
    list_filter = ("course",)

@admin.register(GradeSubmission)
class GradeSubmissionAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "grade", "submitted_by", "submitted_on")
    list_filter = ("course", "grade")
