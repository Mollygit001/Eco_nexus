from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import models

from .models import (
    EnvCourse, CourseModule, LessonContent, Quiz, Question, 
    Choice, Attempt, GamificationLedger
)
from accounts.models import StudentProfile


class EnvCourseListView(ListView):
    """
    Display all available environmental courses
    """
    model = EnvCourse
    template_name = 'lms/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check which courses user is enrolled in (for future enhancement)
        context['total_courses'] = EnvCourse.objects.count()
        
        return context

    def get_queryset(self):
        queryset = EnvCourse.objects.prefetch_related('modules')
        
        # Search by title or description
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) |
                models.Q(description__icontains=search)
            )
        
        return queryset.order_by('-id')


class EnvCourseDetailView(DetailView):
    """
    Display detailed information about an environmental course
    """
    model = EnvCourse
    template_name = 'lms/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Get all modules for this course
        context['modules'] = course.modules.all().order_by('order')
        context['modules_count'] = context['modules'].count()
        
        # Get total lessons
        lesson_count = 0
        for module in context['modules']:
            lesson_count += module.contents.count()
        context['lesson_count'] = lesson_count
        
        # Get related UMS course if exists
        if course.related_ums_course:
            context['related_ums_course'] = course.related_ums_course
        
        return context


class CourseModuleDetailView(DetailView):
    """
    Display module content and lessons
    """
    model = CourseModule
    template_name = 'lms/module_detail.html'
    context_object_name = 'module'
    pk_url_kwarg = 'module_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        
        # Get all lesson content for this module
        context['lessons'] = module.contents.all().order_by('id')
        
        # Get all quizzes for this module
        context['quizzes'] = module.quizzes.all()
        
        # Get parent course
        context['course'] = module.course
        
        # Check user progress if authenticated
        if self.request.user.is_authenticated:
            try:
                student_profile = self.request.user.student_profile
                context['student_profile'] = student_profile
                
                # Check completed quizzes
                completed_quizzes = Attempt.objects.filter(
                    student=student_profile,
                    quiz__module=module
                ).values_list('quiz_id', flat=True)
                context['completed_quiz_ids'] = list(completed_quizzes)
            except StudentProfile.DoesNotExist:
                pass
        
        return context


@method_decorator(login_required, name='dispatch')
class QuizView(DetailView):
    """
    Display quiz questions for the student to answer
    """
    model = Quiz
    template_name = 'lms/quiz.html'
    context_object_name = 'quiz'
    pk_url_kwarg = 'quiz_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        
        # Get all questions with their choices
        context['questions'] = quiz.questions.all().prefetch_related('choices')
        context['questions_count'] = context['questions'].count()
        
        # Get parent module and course
        context['module'] = quiz.module
        context['course'] = quiz.module.course
        
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle quiz submission
        """
        quiz = self.get_object()
        
        try:
            student_profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            messages.error(request, "Student profile not found.")
            return redirect('lms:course_list')
        
        # Calculate score
        score = 0
        submitted_answers = {}
        
        questions = quiz.questions.all()
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            
            if selected_choice_id:
                try:
                    choice = Choice.objects.get(id=selected_choice_id, question=question)
                    submitted_answers[question.id] = {
                        'choice': choice,
                        'is_correct': choice.is_correct
                    }
                    
                    if choice.is_correct:
                        score += 1
                except Choice.DoesNotExist:
                    pass
        
        # Create attempt record
        attempt = Attempt.objects.create(
            quiz=quiz,
            student=student_profile,
            score=score
        )
        
        # Create gamification entry
        points_earned = score * 10  # 10 points per correct answer
        GamificationLedger.objects.create(
            student=student_profile,
            event='quiz_completed',
            points=points_earned,
            payload={
                'quiz_id': quiz.id,
                'quiz_title': quiz.title,
                'score': score,
                'total_questions': questions.count()
            }
        )
        
        # Update student gamification points
        total_points = GamificationLedger.objects.filter(
            student=student_profile
        ).aggregate(models.Sum('points'))['points__sum'] or 0
        
        messages.success(request, f"Quiz completed! You scored {score}/{questions.count()}. +{points_earned} points!")
        
        return redirect('lms:quiz_results', quiz_id=quiz.id, attempt_id=attempt.id)


@method_decorator(login_required, name='dispatch')
class QuizResultsView(TemplateView):
    """
    Display quiz results and feedback
    """
    template_name = 'lms/quiz_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        quiz_id = self.kwargs.get('quiz_id')
        attempt_id = self.kwargs.get('attempt_id')
        
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            return context
        
        # Get quiz and attempt
        quiz = get_object_or_404(Quiz, id=quiz_id)
        attempt = get_object_or_404(Attempt, id=attempt_id, student=student_profile, quiz=quiz)
        
        context['quiz'] = quiz
        context['attempt'] = attempt
        context['module'] = quiz.module
        context['course'] = quiz.module.course
        
        # Calculate percentage
        total_questions = quiz.questions.count()
        context['percentage'] = (attempt.score / total_questions * 100) if total_questions > 0 else 0
        context['total_questions'] = total_questions
        
        # Get all questions with correct answers
        context['questions'] = quiz.questions.all().prefetch_related('choices')
        
        # Get all attempts for this quiz by this student
        context['all_attempts'] = Attempt.objects.filter(
            quiz=quiz,
            student=student_profile
        ).order_by('-taken_on')
        
        return context


@method_decorator(login_required, name='dispatch')
class StudentDashboardView(TemplateView):
    """
    Display student learning dashboard with progress and gamification
    """
    template_name = 'lms/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            student_profile = self.request.user.student_profile
        except StudentProfile.DoesNotExist:
            return context
        
        context['student_profile'] = student_profile
        
        # Get all quiz attempts
        attempts = Attempt.objects.filter(student=student_profile).order_by('-taken_on')
        context['recent_attempts'] = attempts[:10]
        context['total_attempts'] = attempts.count()
        
        # Calculate total points and badges
        gamification_entries = GamificationLedger.objects.filter(student=student_profile)
        context['total_points'] = gamification_entries.aggregate(
            models.Sum('points')
        )['points__sum'] or 0
        
        # Get unique badges
        badges = gamification_entries.filter(
            badge_awarded__isnull=False
        ).values_list('badge_awarded', flat=True).distinct()
        context['badges'] = list(badges)
        context['badges_count'] = len(context['badges'])
        
        # Calculate average quiz score
        if attempts.exists():
            avg_score = sum(a.score for a in attempts) / attempts.count()
            context['average_score'] = round(avg_score, 2)
        else:
            context['average_score'] = 0
        
        # Get quiz statistics
        context['quiz_stats'] = {
            'total_completed': attempts.count(),
            'perfect_scores': attempts.filter(score=models.F('quiz__questions__count')).count(),
        }
        
        return context


# Backward compatibility wrappers for legacy URL patterns
def env_course_list(request):
    """Legacy wrapper for EnvCourseListView"""
    view = EnvCourseListView.as_view()
    return view(request)
