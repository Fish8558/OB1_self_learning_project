import factory
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework.test import APIClient

from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика создания пользователей"""

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.LazyAttribute(lambda _: fake.unique.email())
    user_name = factory.LazyAttribute(lambda _: fake.unique.user_name())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:15])
    city = factory.LazyAttribute(lambda _: fake.city())
    password = factory.PostGenerationMethodCall("set_password", "password")

    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def save_user(self, create, extracted, **kwargs):
        if create:
            self.save()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_admin():
    """Фикстура создания администратора"""
    return UserFactory.create(role=User.UsersRolesChoices.ADMIN, is_staff=True, is_superuser=True)


@pytest.fixture
def user_professor():
    """Фикстура создания преподавателя"""
    return UserFactory.create(role=User.UsersRolesChoices.PROFESSOR, is_staff=True)


@pytest.fixture
def user_student():
    """Фикстура создания студента"""
    return UserFactory.create(role=User.UsersRolesChoices.STUDENT)


@pytest.fixture
def users_list(user_admin, user_professor, user_student):
    """Фикстура создания списка пользователей"""
    return [user_admin, user_professor, user_student]


@pytest.fixture
def reset_password_data(user_student):
    """Фикстура создания данных для сброса пароля"""
    uid = urlsafe_base64_encode(force_bytes(user_student.pk))
    token = default_token_generator.make_token(user_student)
    return {
        "uid": uid,
        "token": token,
        "new_password": "newpass@123"
    }
