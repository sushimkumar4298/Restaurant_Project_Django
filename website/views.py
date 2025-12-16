from django.shortcuts import render, redirect
from .models import Category, MenuItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

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

def user_logout(request):
    logout(request)
    return redirect('home')




def index(request):
    return render(request, 'website/index.html')




def about(request):
    return render(request, 'website/about.html')


def book(request):
    return render(request, 'website/book.html')


def menu_view(request):
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'website/menu.html', {
        'categories': categories
    })


from django.contrib.auth.decorators import login_required
@login_required
def user_profile(request):
    return render(request, 'website/profile.html')