from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from courses.models import Course, Module, Lesson, LessonTest, Question, Answer
from courses.paginations import CustomPagination
from courses.serializers import CourseSerializer, ModuleSerializer, LessonSerializer, LessonTestSerializer, \
    QuestionSerializer, AnswerSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Представление курсов"""
    serializer_class = CourseSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all().order_by('title')


class ModuleViewSet(viewsets.ModelViewSet):
    """Представление модулей"""
    serializer_class = ModuleSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Module.objects.all().order_by('title')


class LessonViewSet(viewsets.ModelViewSet):
    """Представление уроков"""
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Lesson.objects.all().order_by('title')


class LessonTestViewSet(viewsets.ModelViewSet):
    """Представление теста уроков"""
    serializer_class = LessonTestSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = LessonTest.objects.all().order_by('title')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def check_answers(self, request, pk=None):
        test = self.get_object()
        answers = request.data.get('answers', {})

        if not isinstance(answers, dict):
            return Response(
                {"detail": "Неверный формат для ответов. Должен быть словарь.."},
                status=status.HTTP_400_BAD_REQUEST
            )

        correct_answers = 0
        total_questions = test.questions.count()

        for question in test.questions.all():
            correct_answer = question.answers.filter(is_correct=True).first()
            user_answer = answers.get(str(question.id))
            if correct_answer and user_answer == correct_answer.text:
                correct_answers += 1

        return Response({
            "correct_answers": correct_answers,
            "total_questions": total_questions
        })


class QuestionViewSet(viewsets.ModelViewSet):
    """Представление вопросов"""
    serializer_class = QuestionSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all().order_by('text')


class AnswerViewSet(viewsets.ModelViewSet):
    """Представление ответов"""
    serializer_class = AnswerSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Answer.objects.all().order_by('text')
