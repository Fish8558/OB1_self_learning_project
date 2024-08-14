from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from config import settings
from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Класс сериализатор регистрации пользователя"""
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def save(self, *args, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают!")

        user = User.objects.create(
            email=self.validated_data.get('email'),
            user_name=self.validated_data.get('user_name'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            phone=self.validated_data.get('phone', None),
            city=self.validated_data.get('city', None),
            role=self.validated_data.get('role'),
        )

        user.is_active = True
        if user.role == User.UsersRolesChoices.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        elif user.role == User.UsersRolesChoices.PROFESSOR:
            user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатор пользователя (просмотр, изменение)"""

    class Meta:
        model = User
        fields = '__all__'


class UserPasswordResetSerializer(serializers.Serializer):
    """Класс сериализатор сброса пароля пользователя"""
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email не зарегистрирован.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid, token=token)
        send_mail(
            'Сброс пароля',
            f'Перейдите по следующей ссылке, чтобы сбросить пароль: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    """Класс сериализатор подтверждения сброса пароля пользователя"""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=7)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"detail": "Невалидный UID."})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Невалидный токен."})
        attrs['user'] = user
        return attrs

    def save(self):
        uid = self.validated_data['uid']
        user_id = urlsafe_base64_decode(uid)
        new_password = self.validated_data['new_password']
        user = User.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
