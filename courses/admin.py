from django.contrib import admin

from courses.models import Course, Module, Lesson, LessonTest, Question, Answer


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('title',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'module', 'created_at')
    list_filter = ('module',)
    search_fields = ('title',)


@admin.register(LessonTest)
class LessonTestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'lesson')
    list_filter = ('lesson',)
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'lesson_test')
    list_filter = ('lesson_test',)
    search_fields = ('text',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'question', 'is_correct')
    list_filter = ('question',)
    search_fields = ('text',)
