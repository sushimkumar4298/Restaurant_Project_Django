from django.contrib import admin
from .models import Category, MenuItem, HeroSection, Cart, CartItem
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
    
    
admin.site.register(HeroSection)    



class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    inlines = [CartItemInline]
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'menu_item', 'quantity')