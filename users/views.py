from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAdminUser
from courses.paginations import CustomPagination
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserRegistrationSerializer, UserSerializer, UserPasswordResetSerializer, \
    UserPasswordResetConfirmSerializer


class UserListAPIView(generics.ListAPIView):
    """Представление для просмотра пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.order_by('id')
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination


class UserRegistrationAPIView(generics.CreateAPIView):
    """Представление для создания пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Пользователь успешно зарегистрирован!"},
                                 status=status.HTTP_201_CREATED)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Представление для редактирования пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class UserPasswordResetAPIView(generics.GenericAPIView):
    """Представление для сброса пароля пользователя"""
    serializer_class = UserPasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Ссылка для сброса пароля отправлена на почту."},
                                 status=status.HTTP_200_OK)


class UserPasswordResetConfirmAPIView(generics.GenericAPIView):
    """Представление для подтверждения сброса пароля пользователя"""
    serializer_class = UserPasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **kwargs})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Пароль успешно сброшен!"},
                                 status=status.HTTP_200_OK)
