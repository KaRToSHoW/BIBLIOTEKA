from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='user_logout'),
]
