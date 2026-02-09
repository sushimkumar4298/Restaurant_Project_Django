from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CategoryForm
from .models import Category, MenuItem, HeroSection, Cart, CartItem, Address

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal




def admin_login(request):
    # If already logged in as admin, redirect
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('restaurant_admin_dashboard')

    if request.method == "POST":
        email_or_username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email_or_username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('restaurant_admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'restaurant_admin/login.html')



def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def user_login(request):
    # ✅ Block logged-in users from login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'website/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'website/signup.html')





def index(request):
    hero = HeroSection.objects.all()  # fetch first hero section
    return render(request, 'website/index.html', {
        'hero': hero
    })





def about(request):
    return render(request, 'website/about.html')

def book(request):
    return render(request, 'website/book.html', 
    )


def menu_view(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'website/menu.html', {
        'categories': categories
    })



from django.contrib.auth.decorators import login_required
@login_required
def user_profile(request):
    return render(request, 'website/profile.html')


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('menu')



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    # Calculate total price for each item
    for item in cart_items:
        item.total = item.menu_item.price * item.quantity  # add a temporary attribute
    
    total_price = sum(item.total for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    
    return render(request, 'website/cart.html', context)



@login_required
def remove_from_cart(request, item_id):
    # Get the cart for the logged-in user
    cart = get_object_or_404(Cart, user=request.user)
    
    # Get the CartItem
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    
    # Delete the item
    cart_item.delete()
    
    return redirect('cart')

@login_required
def add_to_cart_ajax(request):
    item_id = request.POST.get('item_id')
    menu_item = MenuItem.objects.get(id=item_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return JsonResponse({
        'quantity': cart_item.quantity,
        'cart_count': cart.items.count()
    })
    
    
@login_required
def increase_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # 🔒 Prevent quantity going below 1
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')

@login_required
def Checkout_view(request):
    addresses = request.user.addresses.all()

    if request.method == "POST":
        selected_address = request.POST.get("selected_address")

        # If user selected existing address
        if selected_address:
            address = Address.objects.get(id=selected_address, user=request.user)
        else:
            # Create new address
            address = Address.objects.create(
                user=request.user,
                full_name=request.POST['full_name'],
                phone=request.POST['phone'],
                address_line=request.POST['address_line'],
                city=request.POST['city'],
                state=request.POST['state'],
                pincode=request.POST['pincode']
            )

        # Save address ID in session for next step
        request.session['address_id'] = address.id

        return redirect('payment')  # next step (later)

    return render(request, 'website/checkout.html', {
        'addresses': addresses
    })

@login_required
def checkout(request):
    if request.method == "POST":
        # Unset previous default if current is default
        if request.POST.get('is_default'):
            Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line=request.POST.get('address_line'),
            landmark=request.POST.get('landmark', ''),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            instructions=request.POST.get('instructions', ''),
            is_default=True if request.POST.get('is_default') else False
        )
        return redirect('order_summary')  # or next step in checkout

    return render(request, 'website/checkout.html')

@login_required
def payment(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()   # cleaner & correct

    # ✅ FIXED: use menu_item instead of product
    total = sum(item.quantity * item.menu_item.price for item in cart_items)

    if request.method == "POST":
        # Razorpay logic will go here next
        pass

    return render(request, 'website/payment.html', {
        'cart_items': cart_items,
        'total': total
    })
    
    
def is_admin(user):
    return user.is_staff


@login_required(login_url='/admin-login/')
@user_passes_test(is_admin)
def restaurant_admin_dashboard(request):
    context = {
        'total_categories': Category.objects.count(),
        'total_menu_items': MenuItem.objects.count(),
        'total_carts': Cart.objects.count(),
    }
    return render(request, 'restaurant_admin/dashboard.html', context)

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Category.objects.all()
    return render(request, 'restaurant_admin/categories.html', {'categories': categories})


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_menu_items(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'restaurant_admin/menu_items.html', {'categories': categories})


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_add_category(request):
    from .forms import CategoryForm

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully")
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    return render(request, 'restaurant_admin/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })

    
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_edit_category(request, pk):
    from .forms import CategoryForm
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully")
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'restaurant_admin/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })
    
    
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('admin_categories')
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_add_menu_item(request, category_id=None):
    from .forms import MenuItemForm
    from .models import Category

    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            if category:
                menu_item.category = category
            menu_item.save()
            messages.success(request, "Menu item added successfully")
            return redirect('admin_menu_items')
    else:
        form = MenuItemForm()
        if category:
            form.fields['category'].initial = category

    return render(request, 'restaurant_admin/menu_item_form.html', {
        'form': form,
        'title': 'Add Menu Item',
        'category': category
    })


def category_add(request):
    form = CategoryForm()
    return render(request, 'restaurant_admin/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_edit_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully")
            return redirect('admin_menu_items')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'restaurant_admin/menu_item_form.html', {'form': form, 'title': 'Edit Menu Item'})

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin)
def admin_delete_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    menu_item.delete()
    messages.success(request, "Menu item deleted successfully")
    return redirect('admin_menu_items')
