from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from src.reviews.models import Comment, Review
from src.titles.models import Title


class ReviewSerializer(serializers.ModelSerializer):
    """CRUD отзывов к произведениям."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title = get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id')
            )
            if request.user.reviews.filter(title=title).exists():
                raise serializers.ValidationError(
                    'Вы уже написали отзыв к этому произведению!')
            return data
        return data


class CommentSerializer(serializers.ModelSerializer):
    """CRUD комментариев к отзывам."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
