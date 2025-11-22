from django.contrib import admin
from .models import Employer, JobPosting, Application, GreenProfile, EmployerProfile


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('employer', 'bio', 'created_at')
    search_fields = ('employer__company_name',)
    list_filter = ('created_at',)
    readonly_fields = ('employer', 'created_at')
    ordering = ('-created_at',)


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'location', 'salary', 'category', 'created_at')
    search_fields = ('title', 'role', 'description', 'category')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Job Details', {
            'fields': ('employer', 'title', 'role', 'category', 'location', 'salary')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'applied_at')
    search_fields = ('student__student_id', 'job__title')
    list_filter = ('applied_at', 'job__category')
    readonly_fields = ('applied_at', 'student', 'job')
    ordering = ('-applied_at',)
    fieldsets = (
        ('Applicant & Job', {
            'fields': ('student', 'job')
        }),
        ('Application Content', {
            'fields': ('cover_letter',)
        }),
        ('Application Date', {
            'fields': ('applied_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(GreenProfile)
class GreenProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'sustainability_score', 'last_updated')
    search_fields = ('student__student_id',)
    list_filter = ('last_updated',)
    ordering = ('-last_updated',)



# Register Employer with correct fields
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'website', 'verified')
    search_fields = ('company_name',)
