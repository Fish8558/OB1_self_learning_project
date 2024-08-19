from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from courses.models import Course, Module, Lesson, LessonTest, Question, Answer
from courses.paginations import CustomPagination
from courses.serializers import CourseSerializer, ModuleSerializer, LessonSerializer, LessonTestSerializer, \
    QuestionSerializer, AnswerSerializer
from users.permissions import IsOwnerOrAdminCourses


class CourseViewSet(viewsets.ModelViewSet):
    """Представление курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdminUser()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ModuleViewSet(viewsets.ModelViewSet):
    """Представление модулей"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    """Представление уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()


class LessonTestViewSet(viewsets.ModelViewSet):
    """Представление теста уроков"""
    queryset = LessonTest.objects.all()
    serializer_class = LessonTestSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def check_answers(self, request, pk=None):
        test = self.get_object()
        answers = request.data.get('answers', {})
        correct_answers = 0

        for question in test.questions.all():
            correct_answer = question.answers.filter(is_correct=True).first()
            if answers.get(str(question.id)) == correct_answer.text:
                correct_answers += 1

        return Response({
            "correct_answers": correct_answers,
            "total_questions": test.questions.count()
        })


class QuestionViewSet(viewsets.ModelViewSet):
    """Представление вопросов"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()


class AnswerViewSet(viewsets.ModelViewSet):
    """Представление ответов"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdminCourses()]
        return super().get_permissions()
