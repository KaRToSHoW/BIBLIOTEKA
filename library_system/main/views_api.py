from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Genre, Comment
from .serializers import BookSerializer, GenreSerializer, CommentSerializer
from rest_framework.permissions import AllowAny

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(methods=['GET'], detail=False)
    def filter_books_by_genre(self, request):
        genre_id = request.query_params.get('genre', None)
        if genre_id:
            books = Book.objects.filter(genres__id=genre_id)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        return Response({"message": "Genre ID not provided"}, status=400)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    @action(methods=['POST'], detail=True)
    def add_comment(self, request, pk=None):
        book = self.get_object()  # Получаем книгу по pk

        # Проверяем, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            return Response({"message": "You must be logged in to comment"}, status=403)

        comment_data = request.data.get('comment')
        if comment_data:
            # Создаем комментарий от имени аутентифицированного пользователя
            comment = Comment.objects.create(
                user=request.user,
                book=book,
                content=comment_data
            )
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=201)
        return Response({"message": "Comment content is required"}, status=400)
