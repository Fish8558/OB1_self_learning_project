from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Модель курса"""
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to="courses/course/", default='courses/course/course_example.jpg', **NULLABLE,
                                verbose_name="Превью")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Module(models.Model):
    """Модель модуля курса"""
    title = models.CharField(max_length=200, verbose_name='Название модуля')
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс')
    preview = models.ImageField(upload_to="courses/module/", default='courses/module/module_example.jpg', **NULLABLE,
                                verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


class Lesson(models.Model):
    """Модель урока модуля"""
    title = models.CharField(max_length=200, verbose_name='Название урока')
    content = models.TextField(verbose_name="Контент")
    preview = models.ImageField(upload_to="courses/lesson/", default='courses/lesson/lesson_example.jpg', **NULLABLE,
                                verbose_name="Превью")
    url = models.CharField(max_length=200, **NULLABLE, verbose_name="Ссылка на видео")
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE, verbose_name='Модуль')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonTest(models.Model):
    """Модель теста для урока"""
    title = models.CharField(max_length=200, verbose_name='Название теста')
    lesson = models.ForeignKey(Lesson, related_name='lessons_test', on_delete=models.CASCADE, verbose_name='Материал')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    """Модель вопроса для теста"""
    text = models.TextField(verbose_name='Текст вопроса')
    lesson_test = models.ForeignKey(LessonTest, related_name='questions', on_delete=models.CASCADE, verbose_name='Тест')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """Модель ответа на вопрос"""
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name='Правильность ответа')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
