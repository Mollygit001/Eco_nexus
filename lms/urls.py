from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # Course listing and details
    path('courses/', views.EnvCourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/', views.EnvCourseDetailView.as_view(), name='course_detail'),
    
    # Module and content
    path('modules/<int:module_id>/', views.CourseModuleDetailView.as_view(), name='module_detail'),
    
    # Quiz operations
    path('quiz/<int:quiz_id>/', views.QuizView.as_view(), name='quiz'),
    path('quiz/<int:quiz_id>/results/<int:attempt_id>/', views.QuizResultsView.as_view(), name='quiz_results'),
    
    # Student dashboard
    path('dashboard/', views.StudentDashboardView.as_view(), name='dashboard'),
    
    # Legacy URLs for backward compatibility
    path('env-courses/', views.env_course_list, name='env_course_list'),
]