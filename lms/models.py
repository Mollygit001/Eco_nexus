from django.db import models


class EnvCourse(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    related_ums_course = models.ForeignKey('ums.Course', on_delete=models.SET_NULL, null=True, blank=True)
    points_reward = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class CourseModule(models.Model):
    course = models.ForeignKey(EnvCourse, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} / {self.title}"


class LessonContent(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=20, choices=[('video', 'Video'), ('text', 'Text')])
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    taken_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} -> {self.quiz} ({self.score})"


class GamificationLedger(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    event = models.CharField(max_length=100)  # e.g., 'quiz_completed', 'module_finished'
    payload = models.JSONField(default=dict, blank=True)  # uses JSONB on Postgres
    points = models.IntegerField(default=0)
    badge_awarded = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_id} {self.event} +{self.points}"
