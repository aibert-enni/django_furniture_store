from django.shortcuts import redirect, render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse


from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm

def login(req):
    if req.method == 'POST':
        form = UserLoginForm(data=req.POST)
        if form.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(req, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm() 

    context = {
        'title': 'Home - Авторизация',
        'form': form
    }
    return render(req, 'users/login.html', context)

def registration(req):
    if req.method == "POST":
        form = UserRegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(req, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(req, 'users/registration.html', context)

def profile(req):
    context = {
        'title': 'Home - Кабинет'
    }
    return render(req, 'users/profile.html', context)

def logout(req):
    auth.logout(req)
    return redirect(reverse('main:index'))