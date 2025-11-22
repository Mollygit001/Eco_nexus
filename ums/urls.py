from django.urls import path
from . import views

app_name = 'ums'

urlpatterns = [
    # Course listing and detail
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Enrollment management
    path('courses/<int:course_id>/enroll/', views.EnrollCourseView.as_view(), name='enroll'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll_legacy'),  # Legacy support
    path('enrollment/<int:enrollment_id>/unenroll/', views.UnenrollCourseView.as_view(), name='unenroll'),
    
    # Student dashboards
    path('my-enrollments/', views.MyEnrollmentsView.as_view(), name='my_enrollments'),
    path('my-grades/', views.MyGradesView.as_view(), name='my_grades'),
]