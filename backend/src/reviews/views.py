from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from src.base.permissions import IsAuthorOrAdminOrReadOnly
from src.reviews.models import Review
from src.reviews.serializers import CommentSerializer, ReviewSerializer
from src.titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """CRUD отзывов к произведениям."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_title_or_404(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_or_404().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_or_404()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD комментариев к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_review_or_404(self):
        return get_object_or_404(
            Review,
            title=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review_or_404().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review_or_404()
        )
