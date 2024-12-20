from rest_framework import serializers
from .models import Book, Genre, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Отображение имени пользователя (или email)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # Сериализация жанров, связанных с книгой
    comments = CommentSerializer(many=True, read_only=True)  # Сериализация комментариев, связанных с книгой

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'description', 'published_date', 'date', 'genres', 'comments']
