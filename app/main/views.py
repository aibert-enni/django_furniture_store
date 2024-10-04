from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories


# Create your views here.
class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'Магазин мебели HOME'
        return context

# def index(req):

#     context = {
#         'title': 'Home - Главная',
#         'content': 'Магазин мебели HOME',
#     }
#     return render(req, 'main/index.html', context)

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = 'О нас'
        context['text_on_page'] = "Добро пожаловать в наш интернет-магазин мебели! Мы предлагаем широкий ассортимент стильной и функциональной мебели для любого интерьера. У нас вы найдете everything — от уютных диванов и элегантных столов до стильных стульев и практичных шкафов."
        return context

# def about(req):
#     context = {
#         'title': 'Home - О нас',
#         'content': 'О нас',
#         'text_on_page': "Добро пожаловать в наш интернет-магазин мебели! Мы предлагаем широкий ассортимент стильной и функциональной мебели для любого интерьера. У нас вы найдете everything — от уютных диванов и элегантных столов до стильных стульев и практичных шкафов."
#     }
#     return render(req, 'main/about.html', context)