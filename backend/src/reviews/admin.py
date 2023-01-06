from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    """Категории."""
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """Жанры."""
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ReviewInline(admin.TabularInline):
    """Вывод отзывов на странице произведения."""
    model = Review
    extra = 0
    readonly_fields = ('author',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Произведение."""
    list_display = ('id', 'name', 'year', 'category')
    list_display_links = ('name',)
    list_filter = ('genre', 'category', 'year')
    search_fields = ('year', 'genre__name', 'category__name')
    filter_horizontal = ('genre',)
    inlines = [ReviewInline]
    save_on_top = True


class CommentInline(admin.TabularInline):
    """Вывод комментариев к на странице отзыва к произведению."""
    model = Comment
    extra = 0
    readonly_fields = ('author',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к произведениям."""
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    list_display_links = ('title',)
    list_filter = ('title', 'score')
    search_fields = ('title__name', 'author__username', 'score')
    inlines = [CommentInline]
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии к отзывам."""
    list_display = ('id', 'author', 'review', 'pub_date')
    list_display_links = list_filter = ('author',)
    search_fields = ('author__username',)
