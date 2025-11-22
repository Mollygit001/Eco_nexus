from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Job browsing (students)
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:job_id>/', views.JobDetailView.as_view(), name='job_detail'),
    
    # Applications (students)
    path('jobs/<int:job_id>/apply/', views.JobApplicationCreateView.as_view(), name='apply'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('applications/<int:application_id>/withdraw/', views.WithdrawApplicationView.as_view(), name='withdraw_application'),
    
    # Employer dashboard and management
    path('employer/dashboard/', views.EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('employer/post-job/', views.PostJobView.as_view(), name='post_job'),
    path('employer/applications/<int:application_id>/status/', views.UpdateApplicationStatusView.as_view(), name='update_application_status'),
    
    # Legacy URLs for backward compatibility
    path('apply/<int:job_id>/', views.apply, name='apply_legacy'),
]