from django.contrib import admin
from .models import Genre, Book, Comment, Like
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource
from import_export.fields import Field

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

@admin.register(Genre)
class GenreAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    list_display_links = ('name',)
    readonly_fields = ('created_at',)

# Ресурс экспорта для Book
class BookResource(ModelResource):
    genres = Field(attribute='genres', column_name='Жанры')
    likes_count = Field(attribute='likes_count', column_name='Количество лайков')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publisher', 'published_date', 'genres', 'likes_count', 'date')
        export_order = ('id', 'title', 'author', 'publisher', 'published_date', 'genres', 'likes_count', 'date')

    def dehydrate_genres(self, book):
        """Возвращает список жанров через запятую."""
        return ", ".join([genre.name for genre in book.genres.all()])

    def dehydrate_likes_count(self, book):
        """Возвращает количество лайков."""
        return book.likes_count()

    def get_export_queryset(self, queryset, *args, **kwargs):
        """Фильтрует данные перед экспортом: например, книги с лайками больше 0."""
        return queryset.filter(like__isnull=False).distinct()

@admin.register(Book)
class BookAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = BookResource
    list_display = ('id', 'title', 'author', 'publisher', 'published_date', 'display_genres', 'likes_count', 'date')
    list_filter = ('published_date', 'genres')
    inlines = [CommentInline, LikeInline]
    date_hierarchy = 'published_date'
    filter_horizontal = ('genres',)
    list_display_links = ('title',)
    raw_id_fields = ('genres',)
    readonly_fields = ('date',)
    search_fields = ('title', 'author', 'publisher', 'description')

    @admin.display(description='Жанры')
    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

@admin.register(Comment)
class CommentAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('id', 'user', 'book', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'book__title')
    list_display_links = ('user', 'content',)
    raw_id_fields = ('user', 'book')
    readonly_fields = ('created_at',)


@admin.register(Like)
class LikeAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('id', 'user', 'book', 'liked_at', 'created_at')
    list_filter = ('liked_at', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_display_links = ('user', 'book')
    raw_id_fields = ('user', 'book')
    readonly_fields = ('liked_at', 'created_at')
