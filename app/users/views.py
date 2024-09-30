from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from carts.utils import delete_carts_duplicates
from carts.models import Cart
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

def login(req):
    if req.method == 'POST':
        form = UserLoginForm(data=req.POST)
        if form.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = req.session.session_key

            if user:
                auth.login(req, user)
                messages.success(req,'Вход успешо выполнен')
                
                if session_key:
                   Cart.objects.filter(session_key=session_key).update(user=user)
                   carts = Cart.objects.filter(user=user)
                   delete_carts_duplicates(user, carts)

                redirect_page = req.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(req.POST.get('next'))
                
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

            session_key = req.session.session_key

            auth.login(req, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
                carts = Cart.objects.filter(user=user)
                delete_carts_duplicates(user, carts)

            messages.success(req,'Регистрация и вход успешно выполнены')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(req, 'users/registration.html', context)

@login_required
def profile(req):
    if req.method == "POST":
        print('true')
        form = UserProfileForm(data=req.POST, instance=req.user, files=req.FILES)
        if form.is_valid():
            form.save()
            messages.warning(req,'Данные успешно обновились')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserRegistrationForm(instance=req.user)
        
    context = {
        'title': 'Home - Кабинет',
        'form': form
    }
    return render(req, 'users/profile.html', context)

def users_cart(req):
    return render(req, 'users/users_cart.html')

@login_required
def logout(req):
    auth.logout(req)
    messages.success(req,'Выход успешно выполнен')
    return redirect(reverse('main:index'))