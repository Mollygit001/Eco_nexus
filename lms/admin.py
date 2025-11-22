from django.contrib import admin
from .models import EnvCourse, CourseModule, LessonContent, Quiz, Question, Choice, Attempt, GamificationLedger


@admin.register(EnvCourse)
class EnvCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_ums_course', 'points_reward')
    search_fields = ('title', 'description')
    list_filter = ('related_ums_course',)


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    ordering = ('course', 'order')


@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type')
    search_fields = ('title', 'module__title')
    list_filter = ('content_type', 'module__course')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    search_fields = ('title', 'module__title')
    list_filter = ('module__course',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz',)
    ordering = ('quiz', 'id')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct', 'question__quiz')
    ordering = ('question', 'id')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'score', 'taken_on')
    search_fields = ('quiz__title', 'student__user__username')
    list_filter = ('quiz',)
    readonly_fields = ('taken_on',)
    ordering = ('-taken_on',)


@admin.register(GamificationLedger)
class GamificationLedgerAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'points', 'badge_awarded', 'created_at')
    search_fields = ('student__user__username', 'event', 'badge_awarded')
    list_filter = ('event', 'badge_awarded', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
