from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from src.titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Вывод информации о категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Вывод информации о жанре."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Вывод информации о произведении."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.DecimalField(
        read_only=True, max_digits=4, decimal_places=2
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['name', 'year'],
                message='Запись уже существует!')
        ]


class TitleCreateSerializer(TitleReadSerializer):
    """CRUD произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    def validate(self, data):
        request = self.context['request']
        if request.method in ('POST', 'PUT'):
            genres = self.initial_data['genre']
            if len(genres) < 1:
                raise serializers.ValidationError('Не указаны Жанры!')
            return data
        return data

    def to_representation(self, instance):
        return TitleReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
