from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from .forms import BookForm, CommentForm, BookFormEdit
from .models import Book, Genre, Like
from django.contrib import messages
from django.db.models import Count, Q

def index(request):
    query = request.GET.get('q')  # Поисковый запрос
    filter_by = request.GET.get('filter')  # Фильтр
    genre_filter = request.GET.get('genre')  # Фильтр по жанру

    # Базовый запрос для книг
    books = Book.objects.all()

    # Пример 1: Сложный запрос с Q (AND, OR, NOT)
    # Книги, у которых название содержит запрос ИЛИ описание содержит запрос,
    # НО жанр не относится к выбранному (если фильтр по жанру задан).
    if query:
        query_conditions = Q(title__icontains=query) | Q(description__icontains=query)
        if genre_filter:
            query_conditions &= ~Q(genres__id=genre_filter)
        books = books.filter(query_conditions)

    # Пример 2: Ещё один сложный запрос с Q (AND, OR, NOT)
    # Книги, у которых:
    # - Либо название содержит запрос,
    # - Либо автор содержит запрос,
    # - И жанр совпадает с выбранным (если задан).
    if genre_filter and query:
        advanced_filter = (Q(title__icontains=query) | Q(author__icontains=query)) & Q(genres__id=genre_filter)
        books = books.filter(advanced_filter)

    # Фильтрация по дополнительным критериям
    if filter_by == 'author':
        books = books.order_by('author')
    elif filter_by == 'date':
        books = books.order_by('-date')
    elif filter_by == 'publisher':
        books = books.order_by('publisher')
    elif filter_by == 'likes':
        books = books.annotate(likes_count=Count('like')).order_by('-likes_count')

    # Пагинация
    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Все доступные жанры
    genres = Genre.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
        'genres': genres,
        'selected_genre': genre_filter,  # Выбранный жанр
    }
    return render(request, 'main/index.html', context)


class BooksDetailView(DetailView):
    model = Book
    template_name = 'main/book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['comments'] = book.comments.all()
        context['form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(user=self.request.user, book=book).exists()
        else:
            context['liked'] = False

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
        return redirect('BooksDetail', pk=book.pk)

@login_required
def toggle_like(request, pk):
    book = get_object_or_404(Book, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, book=book)
    if not created:
        like.delete()
        messages.success(request, f'You have unliked "{book.title}".')
    else:
        messages.success(request, f'You have liked "{book.title}".')
    return redirect('BooksDetail', pk=pk)


def about(request):
    return render(request, 'main/about.html')

def addBook(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем книгу, но не подтверждаем связывание жанров
            book = form.save(commit=False)
            book.save()  # Сохраняем книгу, чтобы она получила ID

            # Теперь связываем жанры с книгой
            genres = form.cleaned_data['genres']
            book.genres.set(genres)  # Связываем жанры с книгой
            book.save()  # Обязательно сохраняем изменения

            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'main/addBook.html', {'form': form})

def editBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookFormEdit(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('BooksDetail', pk=book.pk)
    else:
        form = BookFormEdit(instance=book)
    return render(request, 'main/edit_book.html', {'form': form, 'book': book})

def deleteBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('home')
    return render(request, 'main/confirm_delete.html', {'book': book})
