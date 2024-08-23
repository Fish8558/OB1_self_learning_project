from django.contrib import admin
from .models import Course, Module, Lesson, LessonTest, Question, Answer
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(course__owner=request.user)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'module', 'created_at')
    list_filter = ('module',)
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(module__course__owner=request.user)


@admin.register(LessonTest)
class LessonTestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'lesson')
    list_filter = ('lesson',)
    search_fields = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(lesson__module__course__owner=request.user)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'lesson_test')
    list_filter = ('lesson_test',)
    search_fields = ('text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(lesson_test__lesson__module__course__owner=request.user)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'question', 'is_correct')
    list_filter = ('question',)
    search_fields = ('text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs
        return qs.filter(question__lesson_test__lesson__module__course__owner=request.user)
