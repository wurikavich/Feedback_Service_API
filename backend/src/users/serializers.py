from django.conf import settings
from rest_framework import serializers

from src.users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Вывод информации о пользователях."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class AuthSignupSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя по username и email."""

    username = serializers.SlugField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if username.lower() in settings.FORBIDDEN_NAMES:
            raise serializers.ValidationError(
                f"Использовать '{username}' запрещено!")
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f"Пользователь с именем '{username}' уже существует!")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f"Пользователь с почтой '{email}' уже существует!")
        return data
