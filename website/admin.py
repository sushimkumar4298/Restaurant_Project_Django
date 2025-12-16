from django.contrib import admin
from .models import Category, MenuItem
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
 
 
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):   
    list_display = ('title', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('title',)  