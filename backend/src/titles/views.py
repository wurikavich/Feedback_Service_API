from django.db.models import Avg
from rest_framework import viewsets

from src.base.permissions import IsAdminOrReadOnly
from src.titles.filters import TitleFilter
from src.titles.mixins import CreateListDestroyMixins
from src.titles.models import Category, Genre, Title
from src.titles.serializers import (
    CategorySerializer, GenreSerializer,
    TitleCreateSerializer, TitleReadSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """CRUD произведений."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).select_related('category').prefetch_related('genre')
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return TitleCreateSerializer
        return TitleReadSerializer


class GenreViewSet(CreateListDestroyMixins):
    """CRUD жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CreateListDestroyMixins):
    """CRUD категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
