from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserListAPIView, UserRegistrationAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView, UserPasswordResetAPIView, UserPasswordResetConfirmAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('reset_password/', UserPasswordResetAPIView.as_view(), name='password_reset'),
    path('reset_password_confirm/<str:uid>/<str:token>/', UserPasswordResetConfirmAPIView.as_view(),
         name='password_reset_confirm'),
]
