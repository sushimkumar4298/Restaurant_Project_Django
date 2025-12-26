from django.shortcuts import render,get_object_or_404, redirect
from .models import Category, MenuItem, HeroSection, Cart, CartItem, Address
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal



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

        return redirect('order_summary')  # next step (later)

    return render(request, 'website/checkout.html', {
        'addresses': addresses
    })

