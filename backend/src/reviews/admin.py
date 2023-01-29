from django.contrib import admin

from src.reviews.models import Comment, Review


class CommentInline(admin.TabularInline):
    """Вывод комментариев к отзыву."""
    model = Comment
    extra = 0
    readonly_fields = ('author',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к произведениям."""
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    list_display_links = ('title',)
    list_filter = ('score',)
    search_fields = ('title__name', 'author__username')
    inlines = [CommentInline]
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии к отзывам."""
    list_display = ('id', 'author', 'review', 'pub_date')
    list_display_links = ('author',)
    search_fields = ('author__username',)