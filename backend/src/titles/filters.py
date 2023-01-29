from django_filters import rest_framework as filters

from src.titles.models import Category, Genre, Title


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """Поиск по одному или несколькими значениями, разделенными запятыми."""
    pass


class TitleFilter(filters.FilterSet):
    """
    Фильтр для поиска произведений.
    category - фильтрует по полю slug категории
    genre - фильтрует по полю slug жанра
    name - фильтрует по названию произведения
    year - фильтрует по году выпуска, одному или нескольких
    """

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberInFilter(field_name='year', lookup_expr='in')
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        to_field_name='slug')
    genre = filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all(),
        label='Genres')

    class Meta:
        model = Title
        fields = '__all__'
