from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
# Create your views here.
from .models import *
from .forms import CreateUserForm, newPostForm

@login_required(login_url='login')
def postNewBlog(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    # else:
    # user = User.objects.get(id=1)
    form = newPostForm()
    form.fields['author'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = newPostForm(request.POST)
        if form.is_valid():
            blog = form.save()
            user = User.objects.get(id=1)
            blog.author = user
            blog.save()
            return redirect('home')
        print("we in IF")
    print("we out IF")
    context = {'form':form}
    return render(request,'accounts/post.html', context=context)
    
# def blogPage(request):
#     return render(request,'accounts/blog.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '  + user)
                
                return redirect('login')
        context = {'form':form}
        print(request.method)
        return render(request, 'accounts/Registration.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
	    if request.method == 'POST':
		    username = request.POST.get('username')
		    password = request.POST.get('password')

		    user = authenticate(request, username=username, password=password)

		    if user is not None:
			    login(request, user)
			    return redirect('home')
		    else:
			    messages.info(request, 'Username OR password is incorrect')

	    context = {}
	    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted'),
        'comments' : Comment.objects.all()
    }
    return render(request, 'accounts/blog.html', context)



def userReturn(request):
    MockUser.objects.all().delete()
    MockUser.objects.bulk_create([
        MockUser(firstName="john", passWord="pass1234"),
        MockUser(firstName="john", passWord="pass1234"),
        MockUser(firstName="john", passWord="pass1234"),
        MockUser(firstName="john", passWord="pass1234"),
        MockUser(firstName="john", passWord="pass1234")
    ])
    users = serializers.serialize("json", MockUser.objects.all())
    return JsonResponse(users, safe=False)