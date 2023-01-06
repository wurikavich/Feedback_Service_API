from django.db.models import Avg, Func
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from src.base.filters import TitleFilter
from src.base.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from src.base.utils import BaseCreateListDestroyViewSet
from src.reviews.models import Category, Genre, Review, Title
from src.reviews.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleCreateSerializer, TitleReadSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """CRUD произведений."""
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleReadSerializer


class GenreViewSet(BaseCreateListDestroyViewSet):
    """CRUD жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseCreateListDestroyViewSet):
    """CRUD категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD отзывов к произведениям."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_title_or_404(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_or_404())

    def get_queryset(self):
        return self.get_title_or_404().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_review_or_404(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review_or_404())

    def get_queryset(self):
        return self.get_review_or_404().comments.all()
