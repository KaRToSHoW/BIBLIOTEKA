from django.test import TestCase
from django.contrib.auth.models import User
from .models import Genre, Book, Comment, Like
from django.utils import timezone

class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Fiction")
        self.assertIsInstance(self.genre.created_at, timezone.datetime)
    
    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Fiction")


class BookModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Book Title",
            author="Author Name",
            published_date="2023-01-01"
        )
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Book Title")
        self.assertEqual(self.book.author, "Author Name")
        self.assertIsInstance(self.book.date, timezone.datetime)
        self.assertIn(self.genre, self.book.genres.all())

    def test_book_str(self):
        self.assertEqual(str(self.book), "Book Title")

    def test_book_likes_count(self):
        user = User.objects.create_user(username='testuser', password='12345')
        Like.objects.create(user=user, book=self.book)
        self.assertEqual(self.book.likes_count(), 1)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title="Book Title",
            author="Author Name",
            published_date="2023-01-01"
        )
        self.comment = Comment.objects.create(
            book=self.book,
            user=self.user,
            content="Great book!"
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Great book!")
        self.assertIsInstance(self.comment.created_at, timezone.datetime)
        self.assertEqual(self.comment.book, self.book)
        self.assertEqual(self.comment.user, self.user)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f'Комментарий от {self.user.username} на {self.book.title}')


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.book = Book.objects.create(
            title="Book Title",
            author="Author Name",
            published_date="2023-01-01"
        )
        self.like = Like.objects.create(
            user=self.user,
            book=self.book
        )

    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.book, self.book)
        self.assertIsInstance(self.like.liked_at, timezone.datetime)
        self.assertIsInstance(self.like.created_at, timezone.datetime)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, book=self.book)
