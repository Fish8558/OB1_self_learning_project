import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from courses.models import Course, Module, Lesson, LessonTest, Question, Answer
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create(email='testuser@gmail.com', user_name='testuser', first_name='First', last_name='Last',
                               role='professor', password='testpass', is_staff=True, is_active=True)


@pytest.fixture
def another_user():
    return User.objects.create(email='anotheruser@gmail.com', user_name='anotheruser', first_name='First',
                               last_name='Last', role='professor', password='anotherpass', is_staff=True,
                               is_active=True)


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def course(user):
    return Course.objects.create(title='Test Course', description='Course description', owner=user)


@pytest.fixture
def module(course):
    return Module.objects.create(title='Test Module', course=course)


@pytest.fixture
def lesson(module):
    return Lesson.objects.create(title='Test Lesson', content='Lesson content', module=module)


@pytest.fixture
def lesson_test(lesson):
    return LessonTest.objects.create(title='Test Lesson Test', lesson=lesson)


@pytest.fixture
def question(lesson_test):
    return Question.objects.create(text='Test Question?', lesson_test=lesson_test)


@pytest.fixture
def answer(question):
    return Answer.objects.create(text='Test Answer', question=question, is_correct=True)


@pytest.mark.django_db
class TestCourseViewSet:

    def test_list_courses(self, authenticated_client):
        url = reverse('courses:course-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_course(self, authenticated_client):
        url = reverse('courses:course-list')
        data = {'title': 'New Course', 'description': 'New course description'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Course'

    def test_retrieve_course(self, authenticated_client, course):
        url = reverse('courses:course-detail', args=[course.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == course.title

    def test_update_course(self, authenticated_client, course):
        url = reverse('courses:course-detail', args=[course.id])
        data = {'title': 'Updated Course Title'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Course Title'

    def test_delete_course(self, authenticated_client, course):
        url = reverse('courses:course-detail', args=[course.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()


@pytest.mark.django_db
class TestModuleViewSet:

    def test_list_modules(self, authenticated_client, course):
        url = reverse('courses:module-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_module(self, authenticated_client, course):
        url = reverse('courses:module-list')
        data = {'title': 'New Module', 'course': course.id}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Module'

    def test_retrieve_module(self, authenticated_client, module):
        url = reverse('courses:module-detail', args=[module.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == module.title

    def test_update_module(self, authenticated_client, module):
        url = reverse('courses:module-detail', args=[module.id])
        data = {'title': 'Updated Module Title'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Module Title'

    def test_delete_module(self, authenticated_client, module):
        url = reverse('courses:module-detail', args=[module.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Module.objects.filter(id=module.id).exists()


@pytest.mark.django_db
class TestLessonViewSet:

    def test_list_lessons(self, authenticated_client, module):
        url = reverse('courses:lesson-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_lesson(self, authenticated_client, module):
        url = reverse('courses:lesson-list')
        data = {'title': 'New Lesson', 'content': 'Lesson content', 'module': module.id}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Lesson'

    def test_retrieve_lesson(self, authenticated_client, lesson):
        url = reverse('courses:lesson-detail', args=[lesson.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == lesson.title

    def test_update_lesson(self, authenticated_client, lesson):
        url = reverse('courses:lesson-detail', args=[lesson.id])
        data = {'title': 'Updated Lesson Title'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Lesson Title'

    def test_delete_lesson(self, authenticated_client, lesson):
        url = reverse('courses:lesson-detail', args=[lesson.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Lesson.objects.filter(id=lesson.id).exists()


@pytest.mark.django_db
class TestLessonTestViewSet:

    def test_list_lesson_tests(self, authenticated_client, lesson):
        url = reverse('courses:lesson_test-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_lesson_test(self, authenticated_client, lesson):
        url = reverse('courses:lesson_test-list')
        data = {'title': 'New Lesson Test', 'lesson': lesson.id}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Lesson Test'

    def test_retrieve_lesson_test(self, authenticated_client, lesson_test):
        url = reverse('courses:lesson_test-detail', args=[lesson_test.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == lesson_test.title

    def test_update_lesson_test(self, authenticated_client, lesson_test):
        url = reverse('courses:lesson_test-detail', args=[lesson_test.id])
        data = {'title': 'Updated Lesson Test Title'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Lesson Test Title'

    def test_delete_lesson_test(self, authenticated_client, lesson_test):
        url = reverse('courses:lesson_test-detail', args=[lesson_test.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not LessonTest.objects.filter(id=lesson_test.id).exists()

    def test_check_answers(self, authenticated_client, lesson_test, question, answer):
        url = reverse('courses:lesson_test-check_answers', args=[lesson_test.id])
        data = {'answers': {str(question.id): 'Test Answer'}}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['correct_answers'] == 1
        assert response.data['total_questions'] == lesson_test.questions.count()

    def test_check_answers_invalid_format(self, authenticated_client, lesson_test):
        url = reverse('courses:lesson_test-check_answers', args=[lesson_test.id])
        data = {'answers': 'invalid_format'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['detail'] == 'Неверный формат для ответов. Должен быть словарь..'


@pytest.mark.django_db
class TestQuestionViewSet:

    def test_list_questions(self, authenticated_client, lesson_test):
        url = reverse('courses:question-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_question(self, authenticated_client, lesson_test):
        url = reverse('courses:question-list')
        data = {'text': 'New Question?', 'lesson_test': lesson_test.id}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'New Question?'

    def test_retrieve_question(self, authenticated_client, question):
        url = reverse('courses:question-detail', args=[question.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == question.text

    def test_update_question(self, authenticated_client, question):
        url = reverse('courses:question-detail', args=[question.id])
        data = {'text': 'Updated Question?'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == 'Updated Question?'

    def test_delete_question(self, authenticated_client, question):
        url = reverse('courses:question-detail', args=[question.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Question.objects.filter(id=question.id).exists()


@pytest.mark.django_db
class TestAnswerViewSet:

    def test_list_answers(self, authenticated_client, question):
        url = reverse('courses:answer-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_answer(self, authenticated_client, question):
        url = reverse('courses:answer-list')
        data = {'text': 'New Answer', 'question': question.id, 'is_correct': True}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'New Answer'

    def test_retrieve_answer(self, authenticated_client, answer):
        url = reverse('courses:answer-detail', args=[answer.id])
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == answer.text

    def test_update_answer(self, authenticated_client, answer):
        url = reverse('courses:answer-detail', args=[answer.id])
        data = {'text': 'Updated Answer', 'is_correct': False}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == 'Updated Answer'

    def test_delete_answer(self, authenticated_client, answer):
        url = reverse('courses:answer-detail', args=[answer.id])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(id=answer.id).exists()


@pytest.mark.django_db
class TestModelStrMethods:
    @pytest.fixture(autouse=True)
    def setUp(self, user):
        self.user = user

        self.course = Course.objects.create(
            title='Test Course',
            description='A description of the test course.',
            owner=self.user
        )
        self.module = Module.objects.create(
            title='Test Module',
            course=self.course
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            content='Content of the test lesson.',
            module=self.module
        )
        self.lesson_test = LessonTest.objects.create(
            title='Test Lesson Test',
            lesson=self.lesson
        )
        self.question = Question.objects.create(
            text='Test Question?',
            lesson_test=self.lesson_test
        )
        self.answer = Answer.objects.create(
            question=self.question,
            text='Test Answer',
            is_correct=True
        )

    def test_course_str(self):
        assert str(self.course) == 'Test Course'

    def test_module_str(self):
        assert str(self.module) == 'Test Module'

    def test_lesson_str(self):
        assert str(self.lesson) == 'Test Lesson'

    def test_lesson_test_str(self):
        assert str(self.lesson_test) == 'Test Lesson Test'

    def test_question_str(self):
        assert str(self.question) == 'Test Question?'

    def test_answer_str(self):
        assert str(self.answer) == 'Test Answer'
