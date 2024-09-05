from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('book/add/', views.addBook, name='addBook'),
    path('book/<int:pk>/', views.BooksDetailView.as_view(), name='BooksDetail'),
    path('book/<int:pk>/edit/', views.editBook, name='editBook'),
    path('book/<int:pk>/delete/', views.deleteBook, name='deleteBook'),
    path('book/<int:pk>/like/', views.toggle_like, name='toggleLike'),
]

