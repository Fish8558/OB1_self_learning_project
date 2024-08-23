from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import CourseViewSet, ModuleViewSet, LessonViewSet, LessonTestViewSet, QuestionViewSet, AnswerViewSet

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'module', ModuleViewSet, basename='module')
router.register(r'lesson', LessonViewSet, basename='lesson')
router.register(r'lesson_test', LessonTestViewSet, basename='lesson_test')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'answer', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson_test/<int:pk>/check_answers/', LessonTestViewSet.as_view({'post': 'check_answers'}),
         name='lesson_test-check_answers'),
]
