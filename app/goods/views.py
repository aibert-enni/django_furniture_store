from django.shortcuts import get_list_or_404, render

from goods.models import Products

# Create your views here.

def catalog(req, category_slug):
    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
    context = {
        'title': 'Home - Каталог',
        'goods': goods
    }
    return render(req, 'goods/catalog.html', context)

def product(req, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {
        'title': 'Home - Товар',
        'product': product
    }
    return render(req, 'goods/product.html', context)