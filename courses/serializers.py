from rest_framework import serializers
from courses.models import Course, Module, Lesson, LessonTest, Question, Answer


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        """Автоматически устанавливаем текущего пользователя как владельца курса"""
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)


class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор модуля"""

    class Meta:
        model = Module
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonTestSerializer(serializers.ModelSerializer):
    """Сериализатор теста урока"""

    class Meta:
        model = LessonTest
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопроса"""

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор ответа"""

    class Meta:
        model = Answer
        fields = '__all__'
