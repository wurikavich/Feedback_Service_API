from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Доступы для моделей: Title, Genre, Category
    Разрешить:
        Чтение: Всем пользователям
        Полный доступ: Администраторы
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            (request.user.is_authenticated and request.user.is_admin)
        )


class AllowAdminOnly(BasePermission):
    """
    Доступы для модели User
    Разрешить:
        Полный доступ: Администраторы
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Доступы для моделей: Review, Comment
    Разрешить:
        Чтение: Всем пользователям
        POST DELETE PATCH: Авторам публикаций
        Полный доступ: Администраторы и модераторы
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS or
            obj.author == request.user or
            request.user.is_moderator or
            request.user.is_admin
        )
