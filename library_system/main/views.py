from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import BookForm, CommentForm, BookFormEdit
from .models import Book, Comment, Like
from django.contrib import messages

def index(request):
    books = Book.objects.order_by('-published_date')
    context = {'books': books}
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
            book = form.save(commit=False)
            book.save()
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
