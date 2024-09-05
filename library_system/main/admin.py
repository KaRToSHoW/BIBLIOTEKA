from django.contrib import admin
from .models import Genre, Book, Comment, Like

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    list_display_links = ('name',)
    readonly_fields = ('created_at',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
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
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'content', 'created_at')  
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'book__title')
    list_display_links = ('user','content',)
    raw_id_fields = ('user', 'book')
    readonly_fields = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'liked_at', 'created_at')
    list_filter = ('liked_at', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_display_links = ('user', 'book')
    raw_id_fields = ('user', 'book')
    readonly_fields = ('liked_at', 'created_at')