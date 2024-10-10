from django.urls import path
from django.views.decorators.cache import cache_page

from main import views

app_name = 'main'
urlpatterns = [
    # path('', cache_page(60 * 15)(views.IndexView.as_view()), name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about')
]