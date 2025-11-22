from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models

from .models import JobPosting, Application, EmployerProfile
from .forms import ApplicationForm, JobPostingForm, JobFilterForm
from accounts.models import StudentProfile


class JobListView(ListView):
    """
    Display all available job postings with pagination and filtering
    """
    model = JobPosting
    template_name = 'careers/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jobs'] = JobPosting.objects.count()
        context['form'] = JobFilterForm(self.request.GET)
        
        return context

    def get_queryset(self):
        queryset = JobPosting.objects.select_related('employer')
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by salary range
        min_salary = self.request.GET.get('min_salary')
        max_salary = self.request.GET.get('max_salary')
        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)
        
        # Search by title, role, location, or description
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(role__icontains=search) |
                models.Q(location__icontains=search) |
                models.Q(employer__company_name__icontains=search) |
                models.Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')


class JobDetailView(DetailView):
    """
    Display detailed information about a specific job posting
    """
    model = JobPosting
    template_name = 'careers/job_detail.html'
    context_object_name = 'job'
    pk_url_kwarg = 'job_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        
        # Get applications count
        context['applications_count'] = job.applications.count()
        
        # Check if current user already applied
        context['user_applied'] = False
        if self.request.user.is_authenticated:
            try:
                student_profile = self.request.user.student_profile
                context['user_applied'] = job.applications.filter(
                    student=student_profile
                ).exists()
            except StudentProfile.DoesNotExist:
                pass
        
        # Get similar jobs from same employer
        context['similar_jobs'] = job.employer.jobs.exclude(id=job.id)[:3]
        
        return context


@method_decorator(login_required, name='dispatch')
class JobApplicationCreateView(CreateView):
    """
    Handle job application submission
    """
    model = Application
    form_class = ApplicationForm
    template_name = 'careers/application_form.html'
    success_url = reverse_lazy('careers:my_applications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('job_id')
        context['job'] = get_object_or_404(JobPosting, id=job_id)
        return context

    def form_valid(self, form):
        job_id = self.kwargs.get('job_id')
        job = get_object_or_404(JobPosting, id=job_id)
        
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(self.request, "Student profile not found.")
            return self.form_invalid(form)
        
        # Check if already applied
        if Application.objects.filter(job=job, student=student_profile).exists():
            messages.warning(self.request, "You have already applied for this job.")
            return redirect('careers:job_detail', job_id=job.id)
        
        # Create application
        application = form.save(commit=False)
        application.job = job
        application.student = student_profile
        application.save()
        
        messages.success(self.request, f"Application submitted for {job.title}!")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MyApplicationsView(TemplateView):
    """
    Display student's job applications and status
    """
    template_name = 'careers/my_applications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            return context
        
        # Get all applications by this student
        applications = Application.objects.filter(
            student=student_profile
        ).select_related('job', 'job__employer').order_by('-applied_at')
        
        context['applications'] = applications
        context['applications_count'] = applications.count()
        
        # Status breakdown
        context['status_breakdown'] = {
            'pending': applications.filter(status='pending').count(),
            'reviewing': applications.filter(status='reviewing').count(),
            'interviewed': applications.filter(status='interviewed').count(),
            'rejected': applications.filter(status='rejected').count(),
            'accepted': applications.filter(status='accepted').count(),
        }
        
        return context


@method_decorator(login_required, name='dispatch')
class WithdrawApplicationView(TemplateView):
    """
    Allow student to withdraw an application
    """
    template_name = 'careers/withdraw_application.html'

    def post(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        
        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('careers:my_applications')
        
        # Get application and verify ownership
        application = get_object_or_404(
            Application,
            id=application_id,
            student=student_profile
        )
        
        # Don't allow withdrawal if already rejected or accepted
        if application.status in ['rejected', 'accepted']:
            messages.error(request, f"Cannot withdraw an {application.status} application.")
            return redirect('careers:my_applications')
        
        job_title = application.job.title
        application.delete()
        
        messages.success(request, f"Application for '{job_title}' withdrawn.")
        return redirect('careers:my_applications')


class EmployerDashboardView(TemplateView):
    """
    Dashboard for employers to post jobs and manage applications
    """
    template_name = 'careers/employer_dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Check if user is employer
        if not hasattr(request.user, 'employer_profile'):
            messages.error(request, "Access denied. Employer profile required.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employer_profile = self.request.user.employer_profile
        
        # Get employer's job postings
        jobs = JobPosting.objects.filter(employer=employer_profile)
        context['jobs'] = jobs
        context['total_jobs_count'] = jobs.count()
        
        # Get all applications for employer's jobs
        applications = Application.objects.filter(
            job__employer=employer_profile
        ).select_related('student', 'job').order_by('-applied_at')
        
        context['applications'] = applications
        context['applications_count'] = applications.count()
        
        # Status breakdown
        context['status_breakdown'] = {
            'pending': applications.filter(status='pending').count(),
            'reviewing': applications.filter(status='reviewing').count(),
            'interviewed': applications.filter(status='interviewed').count(),
            'rejected': applications.filter(status='rejected').count(),
            'accepted': applications.filter(status='accepted').count(),
        }
        
        return context


@method_decorator(login_required, name='dispatch')
class PostJobView(CreateView):
    """
    Allow employers to post new job openings
    """
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'careers/post_job.html'
    success_url = reverse_lazy('careers:employer_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'employer_profile'):
            messages.error(request, "Access denied. Employer profile required.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job = form.save(commit=False)
        job.employer = self.request.user.employer_profile
        job.save()
        messages.success(self.request, f"Job '{job.title}' posted successfully!")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class UpdateApplicationStatusView(TemplateView):
    """
    Allow employers to update application status
    """
    template_name = 'careers/update_application_status.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'employer_profile'):
            messages.error(request, "Access denied. Employer profile required.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        new_status = request.POST.get('status')
        
        employer_profile = request.user.employer_profile
        
        # Verify the employer owns this job posting
        application = get_object_or_404(Application, id=application_id)
        if application.job.employer != employer_profile:
            messages.error(request, "Unauthorized access.")
            return redirect('careers:employer_dashboard')
        
        if new_status in ['pending', 'reviewing', 'interviewed', 'rejected', 'accepted']:
            application.status = new_status
            application.save()
            messages.success(request, f"Application status updated to {new_status}.")
        
        return redirect('careers:employer_dashboard')


# Backward compatibility wrappers
def job_list(request):
    """Legacy wrapper for JobListView"""
    view = JobListView.as_view()
    return view(request)


@login_required
def apply(request, job_id):
    """Legacy wrapper for JobApplicationCreateView"""
    job = get_object_or_404(JobPosting, id=job_id)
    try:
        student_profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('careers:job_list')
    
    # Check if already applied
    if Application.objects.filter(job=job, student=student_profile).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('careers:job_list')
    
    # Create application
    Application.objects.create(job=job, student=student_profile)
    messages.success(request, f"Application submitted for {job.title}!")
    return redirect('careers:job_list')
