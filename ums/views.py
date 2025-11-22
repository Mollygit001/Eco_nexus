from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import models
from django.contrib import messages

from .models import Course, Enrollment, Department, GradeSubmission
from accounts.models import StudentProfile


class CourseListView(ListView):
    """
    Display all available courses with filtering options
    """
    model = Course
    template_name = 'ums/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['semesters'] = Course.objects.values_list('semester', flat=True).distinct()
        
        # Check which courses user is enrolled in
        if self.request.user.is_authenticated:
            try:
                student_profile = self.request.user.student_profile
                enrolled_course_ids = Enrollment.objects.filter(
                    student=student_profile
                ).values_list('course_id', flat=True)
                context['enrolled_course_ids'] = list(enrolled_course_ids)
            except StudentProfile.DoesNotExist:
                context['enrolled_course_ids'] = []
        else:
            context['enrolled_course_ids'] = []
        
        return context

    def get_queryset(self):
        queryset = Course.objects.select_related('department', 'semester', 'instructor')
        
        # Filter by department if provided
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Filter by semester if provided
        semester_id = self.request.GET.get('semester')
        if semester_id:
            queryset = queryset.filter(semester_id=semester_id)
        
        # Search by course code or title
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(code__icontains=search) | 
                models.Q(title__icontains=search)
            )
        
        return queryset.order_by('code')


class CourseDetailView(DetailView):
    """
    Display detailed information about a specific course
    """
    model = Course
    template_name = 'ums/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Get enrolled students count
        context['enrolled_students_count'] = Enrollment.objects.filter(
            course=course
        ).count()
        
        # Check if current user is enrolled
        context['is_enrolled'] = False
        context['user_enrollment'] = None
        
        if self.request.user.is_authenticated:
            try:
                student_profile = self.request.user.student_profile
                enrollment = Enrollment.objects.filter(
                    student=student_profile,
                    course=course
                ).first()
                if enrollment:
                    context['is_enrolled'] = True
                    context['user_enrollment'] = enrollment
            except StudentProfile.DoesNotExist:
                pass
        
        # Get grades if enrolled
        if context['is_enrolled']:
            try:
                student_profile = self.request.user.student_profile
                grade = GradeSubmission.objects.filter(
                    student=student_profile,
                    course=course
                ).first()
                context['grade'] = grade
            except:
                pass
        
        return context


@method_decorator(login_required, name='dispatch')
class EnrollCourseView(View):
    """
    Handle course enrollment for authenticated users
    """
    
    def post(self, request, course_id):
        """
        Enroll student in course
        """
        try:
            # Get student profile
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found. Please complete your profile.")
            return redirect('accounts:profile')
        
        # Get course
        course = get_object_or_404(Course, id=course_id)
        
        # Check if already enrolled
        existing_enrollment = Enrollment.objects.filter(
            student=student_profile,
            course=course
        ).exists()
        
        if existing_enrollment:
            messages.warning(request, f"You are already enrolled in {course.title}")
            return redirect('ums:course_detail', course_id=course_id)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student_profile,
            course=course
        )
        
        messages.success(request, f"Successfully enrolled in {course.title}")
        return redirect('ums:course_detail', course_id=course_id)


@method_decorator(login_required, name='dispatch')
class UnenrollCourseView(View):
    """
    Handle course unenrollment for authenticated users
    """
    
    def post(self, request, enrollment_id):
        """
        Unenroll student from course
        """
        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('accounts:profile')
        
        # Get enrollment
        enrollment = get_object_or_404(
            Enrollment,
            id=enrollment_id,
            student=student_profile
        )
        
        course = enrollment.course
        enrollment.delete()
        
        messages.success(request, f"Unenrolled from {course.title}")
        return redirect('ums:my_enrollments')


@method_decorator(login_required, name='dispatch')
class MyEnrollmentsView(ListView):
    """
    Display all courses the student is enrolled in
    """
    model = Enrollment
    template_name = 'ums/my_enrollments.html'
    context_object_name = 'enrollments'
    paginate_by = 12

    def get_queryset(self):
        """
        Only show enrollments for current user
        """
        try:
            student_profile = self.request.user.student_profile
            return Enrollment.objects.filter(
                student=student_profile
            ).select_related('course__department', 'course__instructor')
        except StudentProfile.DoesNotExist:
            return Enrollment.objects.none()


@method_decorator(login_required, name='dispatch')
class MyGradesView(ListView):
    """
    Display all grades for the student
    """
    model = GradeSubmission
    template_name = 'ums/my_grades.html'
    context_object_name = 'grades'
    paginate_by = 20

    def get_queryset(self):
        """
        Only show grades for current user
        """
        try:
            student_profile = self.request.user.student_profile
            return GradeSubmission.objects.filter(
                student=student_profile
            ).select_related('course__department', 'course__semester')
        except StudentProfile.DoesNotExist:
            return GradeSubmission.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate GPA
        try:
            student_profile = self.request.user.student_profile
            context['gpa'] = student_profile.gpa
        except:
            context['gpa'] = None
        
        return context


# Keep legacy function-based views for backward compatibility
def course_list(request):
    """Legacy view - redirect to class-based view"""
    return CourseListView.as_view()(request)


@login_required
def enroll(request, course_id):
    """Legacy view - redirect to class-based view"""
    return EnrollCourseView.as_view()(request, course_id=course_id)
