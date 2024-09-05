from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField('Жанр', max_length=100)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField('Название книги', max_length=200)
    author = models.CharField('Автор', max_length=200)
    publisher = models.CharField('Издатель', max_length=200, null=True, blank=True)
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    description = models.TextField('Описание книги', null=True, blank=True)
    published_date = models.DateField('Дата издания книги')
    date = models.DateTimeField('Дата добавления', default=timezone.now)
    image = models.FileField('Фото для обложки', upload_to='main/static/main/img', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.like_set.count()

    likes_count.short_description = 'Количество лайков'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField('Комментарий')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.user.username} на {self.book.title}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    liked_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата лайка')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'book')
