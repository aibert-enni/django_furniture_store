from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(req):
    context = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME'
    }
    return render(req, 'main/index.html', context)

def about(req):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': "Добро пожаловать в наш интернет-магазин мебели! Мы предлагаем широкий ассортимент стильной и функциональной мебели для любого интерьера. У нас вы найдете everything — от уютных диванов и элегантных столов до стильных стульев и практичных шкафов."
    }
    return render(req, 'main/about.html', context)