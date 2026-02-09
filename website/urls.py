from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.index, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    
    # User profile / cart
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('ajax/add-to-cart/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.Checkout_view, name='checkout'),
    path('payment/', views.payment, name='payment'),

    # Admin login/logout
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),

    # Admin dashboard
    path('restaurant-admin/', views.restaurant_admin_dashboard, name='restaurant_admin'),
    path('admin/dashboard/', views.restaurant_admin_dashboard, name='restaurant_admin_dashboard'),

    # Categories
    path('restaurant-admin/categories/', views.admin_categories, name='admin_categories'),
    path('restaurant-admin/categories/add/', views.admin_add_category, name='admin_add_category'),
    path('restaurant-admin/categories/edit/<int:pk>/', views.admin_edit_category, name='admin_edit_category'),
    path('restaurant-admin/categories/delete/<int:pk>/', views.admin_delete_category, name='admin_delete_category'),

    # Menu Items
    path('restaurant-admin/menu-items/', views.admin_menu_items, name='admin_menu_items'),
    path('restaurant-admin/menu/add/', views.admin_add_menu_item, name='admin_add_menu_item'),  # optional
    path('restaurant-admin/menu-items/edit/<int:pk>/', views.admin_edit_menu_item, name='admin_edit_menu_item'),
    path('restaurant-admin/menu-items/delete/<int:pk>/', views.admin_delete_menu_item, name='admin_delete_menu_item'),
    path('restaurant-admin/menu/add/<int:category_id>/', views.admin_add_menu_item, name='admin_add_menu_item'),

]
