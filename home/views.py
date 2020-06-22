from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UserUpdateForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Book, Status, Ratings, PredictedBooks
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
# Create your views here.

@login_required(login_url = 'home:login')
def home(request):
    try:
    
        user_intrested_books = get_intrested_books(request)
        all_books = get_all_books(request)
        reading_books = get_reading_books(request)

        if request.method == 'POST':
            test = request.POST['test']
            print(test)

        page = request.GET.get('page', 1)
        paginator = Paginator(all_books, 4)
        paginator_two = Paginator(user_intrested_books, 4)
        paginator_three = Paginator(reading_books, 4)
        
        try:
            all_books = paginator.page(page)
            user_intrested_books = paginator_two.page(page)
            reading_books = paginator_three.page(page)

        except PageNotAnInteger:
            all_books = paginator.page(1)
            user_intrested_books = paginator_two.page(page)
            reading_books = paginator_three.page(page)

        except EmptyPage:
            all_books = paginator.page(paginator.num_pages)

    except:
        redirect('home:home')

    context = {
        'user_intrested_books': user_intrested_books,
        'all_books': all_books,
        'reading_books': reading_books,
        
        
    }
    return render(request, 'home/home.html', context)
	

def login_user(request):
    user = request.user

    if user.is_authenticated:
        logout_user(request)
    else:
        if request.method == 'POST':
           username = request.POST.get('username')
           password = request.POST.get('password')
           user = authenticate(username = username, password = password)

           if user is not None:
            login(request, user)
            return redirect('home:home')
           else:
            messages.info(request, 'Usernmae OR Password is wrong.')

    context = {
    }
    
    return render(request, 'home/login.html', context)

@login_required(login_url = 'home:login')
def logout_user(request):
    logout(request)
    return redirect('home:login')

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user  = form.cleaned_data.get('username')
            password  = form.cleaned_data.get('password1')
            # messages.success(request, 'Account is Created for' + user )
            # return redirect('home:login')
            user = authenticate(username = user, password = password)
            if user is not None:
                login(request, user)
                return redirect('home:afterRegister')
    else:
        form = CreateUserForm()


    context = {
        'form' : form,
    }

    return render(request,'home/register.html',context)

@login_required(login_url = 'home:login')
def afterRegister(request):

    if request.method == 'POST':
        test = request.POST.get('test')
        print(test)
    return render(request,'home/afterRegister.html')

def user_profile(request):

    user_intrested_books = get_intrested_books(request)
    all_books = get_all_books(request)
    reading_books = get_reading_books(request)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_books, 4)
    paginator_two = Paginator(user_intrested_books, 4)
    paginator_three = Paginator(reading_books, 4)
    
    try:
        all_books = paginator.page(page)
        user_intrested_books = paginator_two.page(page)
        reading_books = paginator_three.page(page)

    except PageNotAnInteger:
        all_books = paginator.page(1)
        user_intrested_books = paginator_two.page(page)
        reading_books = paginator_three.page(page)

    except EmptyPage:
        all_books = paginator.page(paginator.num_pages)

    
    context = {
        'user_intrested_books': user_intrested_books,
        'all_books': all_books,
        'reading_books': reading_books,
    }
        
   
    return render(request, 'home/profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        user_form       = UserUpdateForm(data =request.POST or None, instance = request.user)
        profile_form    = UserProfileForm(request.POST, request.FILES, instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f"your account is updated")
            redirect('home:home')
    else:
        user_form       = UserUpdateForm(instance = request.user)
        profile_form    = UserProfileForm(instance = request.user.profile)
        redirect('home:home')
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'home/edit-profile.html', context)


def book_detail(request, id):
    try:

        book = Book.objects.get( id = id)

        book_status = request.POST.get('read_btn')

        print(book_status)

        if book_status is not None:
            Status.objects.create(user = request.user, books = book, status_of_book = book_status)
    except:
        redirect('home:home')
        
    context = {
        'book': book,
    }

    return render(request, 'home/book-detail.html', context)
    
def get_user_books(request):

    user = request.user

    books_of_user = user.book_set.all()

    return list(books_of_user)


def get_intrested_books(request):

    user = request.user

    intrested_books = user.status_set.filter(status_of_book = "1")  # 1 is for intrested in status model

    return list(intrested_books)

def get_all_books(request):

    all_books = Book.objects.all()

    return list(all_books)

def get_reading_books(request):

    user = request.user

    reading_books = user.status_set.filter(status_of_book = "3") 

    return list(reading_books)
