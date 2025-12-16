from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
]
