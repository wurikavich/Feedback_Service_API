from django.contrib import admin

from src.reviews.models import Review
from src.titles.models import Category, Genre, Title


class ReviewInline(admin.TabularInline):
    """Вывод отзывов к произведению."""

    model = Review
    extra = 0
    readonly_fields = ('author',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Произведения."""

    list_display = ('id', 'name', 'year', 'category')
    list_display_links = ('name',)
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    filter_horizontal = ('genre',)
    inlines = [ReviewInline]
    save_on_top = True


@admin.register(Category, Genre)
class GenreCategoryBaseAdmin(admin.ModelAdmin):
    """Базовая панель для моделей: Category, Genre."""

    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_filter = ('name',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
