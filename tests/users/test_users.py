import pytest
from django.test import RequestFactory
from django.urls import reverse
from tests.conftest import UserFactory, fake
from users.models import User
from users.serializers import UserSerializer


@pytest.mark.django_db
class TestUsers:
    """Тестирование приложения Users"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, user_admin, user_professor, user_student):
        self.api_client = api_client
        self.user_admin = user_admin
        self.user_professor = user_professor
        self.user_student = user_student
        self.factory = RequestFactory()

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_admin", 200),
        ("user_professor", 200),
        ("user_student", 403),
        ("anonymous_user", 401),
    ])
    def test_user_list(self, request, api_client, auth_user, users_list, expected_status):
        """
        Тестирование просмотра списка пользователей
        [GET] http://127.0.0.1:8000/users/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client

        response = client.get(reverse('users:user_list'))

        assert response.status_code == expected_status
        if response.status_code == 200:
            print(response.data)
            assert response.data['count'] == len(users_list)

    @pytest.mark.parametrize("role, password2, expected_status, expected_detail", [
        ("admin", "password123", 201, 'Пользователь успешно зарегистрирован!'),
        ("professor", "password123", 201, 'Пользователь успешно зарегистрирован!'),
        ("student", "password123", 201, 'Пользователь успешно зарегистрирован!'),
        ("student", "password321", 400, 'Пароли не совпадают!'),
        ("hacker", "password123", 400, None),
    ])
    def test_user_create(self, api_client, role, password2, expected_status, expected_detail):
        """
        Тестирование создания пользователя
        [POST] http://127.0.0.1:8000/users/create/
        """

        email = "existing_email@example.com"
        if expected_status == 400 and expected_detail == "Данный email уже зарегистрирован!":
            UserFactory.create(email=email)
        else:
            email = fake.email()

        data = {
            "email": email,
            "user_name": fake.unique.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number()[:15],
            "city": fake.city(),
            "role": role,
            "password": "password123",
            "password2": password2
        }

        response = api_client.post(reverse('users:user_register'), data=data, format='json')

        assert response.status_code == expected_status
        if response.status_code == 201:
            assert response.data['detail'] == expected_detail

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 200),
        ("user_admin", "user_professor", 200),
        ("user_admin", "user_student", 200),

        ("user_professor", "user_admin", 403),
        ("user_professor", "user_professor", 200),
        ("user_professor", "user_student", 403),

        ("user_student", "user_admin", 403),
        ("user_student", "user_professor", 403),
        ("user_student", "user_student", 200),

        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_professor", 401),
        ("anonymous_user", "user_student", 401)
    ])
    def test_user_update(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование редактирования пользователя
        [PATCH] http://127.0.0.1:8000/users/update/{int:pk}/
        """
        data = {"first_name": "Новое имя"}
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)

        response = client.patch(reverse('users:user_update', kwargs={'pk': target_user.pk}), data=data,
                                format='json')

        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.data["first_name"] == data["first_name"]

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 200),
        ("user_admin", "user_professor", 200),
        ("user_admin", "user_student", 200),

        ("user_professor", "user_admin", 403),
        ("user_professor", "user_professor", 200),
        ("user_professor", "user_student", 403),

        ("user_student", "user_admin", 403),
        ("user_student", "user_professor", 403),
        ("user_student", "user_student", 200),

        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_professor", 401),
        ("anonymous_user", "user_student", 401)
    ])
    def test_user_detail(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование просмотра пользователя
        [GET] http://127.0.0.1:8000/users/detail/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)
        response = client.get(reverse('users:user_detail', kwargs={'pk': target_user.pk}))

        assert response.status_code == expected_status
        if expected_status == 200:
            expected_data = UserSerializer(target_user).data
            if 'image' in expected_data and expected_data['image']:
                request = self.factory.get('/')
                expected_data['image'] = request.build_absolute_uri(expected_data['image'])
            assert response.data == expected_data

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 204),
        ("user_admin", "user_professor", 204),
        ("user_admin", "user_student", 204),

        ("user_professor", "user_admin", 403),
        ("user_professor", "user_professor", 204),
        ("user_professor", "user_student", 403),

        ("user_student", "user_admin", 403),
        ("user_student", "user_professor", 403),
        ("user_student", "user_student", 204),

        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_professor", 401),
        ("anonymous_user", "user_student", 401)
    ])
    def test_user_destroy(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование удаления пользователя
        [DELETE] http://127.0.0.1:8000/users/delete/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)

        response = client.delete(reverse('users:user_delete', kwargs={'pk': target_user.pk}))

        assert response.status_code == expected_status

    @pytest.mark.parametrize("email, expected_status, expected_detail", [
        ("{user_student_email}", 200, "Ссылка для сброса пароля отправлена на почту."),
        ("not_found@example.com", 400, "Email не зарегистрирован."),
        ("invalid_email", 400, "Введите правильный адрес электронной почты.")
    ])
    def test_user_password_reset(self, api_client, user_student, email, expected_status, expected_detail):
        """
        Тестирование сброса пароля пользователя
        [POST] http://127.0.0.1:8000/users/reset_password/
        """
        if email == "{user_student_email}":
            email = self.user_student.email
        data = {"email": email}
        response = api_client.post(reverse('users:password_reset'), data=data)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.data["detail"] == expected_detail
        else:
            if "email" in response.data:
                assert expected_detail in response.data["email"]

    @pytest.mark.parametrize("uid, token, new_password, expected_status, expected_detail", [
        ("valid_uid", "valid_token", "password123", 200, "Пароль успешно сброшен!"),
        ("invalid_uid", "valid_token", "password123", 400, "Невалидный UID."),
        ("valid_uid", "invalid_token", "password123", 400, "Невалидный токен."),
        ("valid_uid", "valid_token", None, 400, "Обязательное поле."),

    ])
    def test_user_password_reset_confirm(self, api_client, user_student, reset_password_data, uid, token, new_password,
                                         expected_status, expected_detail):
        """
        Тестирование подтверждения сброса пароля пользователя
        [POST] http://127.0.0.1:8000/users/reset_password_confirm/{str:uid}/{str:token}/
        """
        if uid == "valid_uid":
            uid = reset_password_data["uid"]
        if token == "valid_token":
            token = reset_password_data["token"]

        data = {'uid': uid, 'token': token, "new_password": new_password} if new_password is not None else {}
        response = api_client.post(reverse('users:password_reset_confirm',
                                           kwargs={'uid': uid, 'token': token}), data=data, format='json')
        assert response.status_code == expected_status

        if expected_status == 200:
            assert response.data['detail'] == expected_detail
            self.user_student.refresh_from_db()
            assert self.user_student.check_password(new_password)
        else:
            assert expected_detail in str(response.data)


@pytest.mark.django_db
class TestUsersModel:
    """Тестирование модели приложения users"""

    def test_user_model_str(self, user_student):
        """Тестирование метода str у модели User"""
        user = User.objects.get(pk=user_student.pk)
        assert str(user) == user_student.email