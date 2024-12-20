from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views_api import BookViewSet, GenreViewSet
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register(r'books', BookViewSet)  # Регистрируем ViewSet для Book
router.register(r'genres', GenreViewSet)  # Регистрируем ViewSet для Genre

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', include(router.urls)),
    path('about/', views.about, name='about'),
    path('book/add/', views.addBook, name='addBook'),
    path('book/<int:pk>/', views.BooksDetailView.as_view(), name='BooksDetail'),
    path('book/<int:pk>/edit/', views.editBook, name='editBook'),
    path('book/<int:pk>/delete/', views.deleteBook, name='deleteBook'),
    path('book/<int:pk>/like/', views.toggle_like, name='toggleLike'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
