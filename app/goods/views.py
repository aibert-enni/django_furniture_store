from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Products

# Create your views here.

def catalog(req, category_slug):

    page = req.GET.get('page', 1)
    on_sale = req.GET.get('on_sale', False)
    order_by = req.GET.get('order_by', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(page)

    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug
    }
    return render(req, 'goods/catalog.html', context)

def product(req, product_slug):
    product = Products.objects.get(slug=product_slug)
    context = {
        'title': 'Home - Товар',
        'product': product
    }
    return render(req, 'goods/product.html', context)