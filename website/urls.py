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
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('ajax/add-to-cart/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.Checkout_view, name='checkout'),
]