from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import CourseViewSet, ModuleViewSet, LessonViewSet, LessonTestViewSet, QuestionViewSet, AnswerViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'lesson_tests', LessonTestViewSet, basename='lesson_tests')
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
]