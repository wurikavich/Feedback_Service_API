from django_filters import rest_framework as filters

from ..reviews.models import Category, Genre, Title


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class TitleFilter(filters.FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all(),
        label='Categories')
    genre = filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all(),
        label='Genres')
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains")
    year = NumberInFilter(field_name="year", lookup_expr="in")

    class Meta:
        model = Title
        fields = "__all__"
