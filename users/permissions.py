from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOrAdmin(BasePermission):
    """Проверка прав на владельца, администратора"""
    message = "Доступ запрещен! Данное действие доступно владельцу или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_superuser


class IsOwnerOrAdminCourses(IsAuthenticated):
    """Проверка прав доступа к представлениям"""
    message = "Доступ запрещен! Данное действие доступно владельцу или администратору!"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser
