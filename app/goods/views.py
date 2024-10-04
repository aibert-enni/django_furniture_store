from typing import Any
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.shortcuts import get_list_or_404, render

from goods.utils import q_search
from goods.models import Categories, Products


class CatalogView(ListView):
  model = Products
  # queryset = Products.objects.all().order_by('-id')
  template_name = 'goods/catalog.html'
  context_object_name = 'goods'
  paginate_by = 3
  allow_empty = False

  def get_queryset(self):
    category_slug = self.kwargs.get('category_slug')
    on_sale = self.request.GET.get('on_sale', False)
    order_by = self.request.GET.get('order_by', None)
    query = self.request.GET.get('q', None)

    if category_slug == 'all':
        goods = super().get_queryset()
    elif query:
        goods = q_search(query)
    else:
       goods = super().get_queryset().filter(category__slug=category_slug)
       if not goods.exists():
        raise Http404()

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    # self.categories = Categories.objects.all()

    return goods
  

  def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    context = super().get_context_data(**kwargs)
    context['title'] = 'Home - Каталог'
    context['slug_url'] = self.kwargs.get('category_slug')
    context['categories'] = Categories.objects.all() #self.categories
    return context



class ProductView(DetailView):
   template_name = 'goods/product.html'
   slug_url_kwarg = 'product_slug'
   context_object_name = 'product'

   def get_object(self, queryset=None):
    product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
    return product
   
   def get_context_data(self, **kwargs: Any):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Home - Товар'
      return context
   
   
   # model = Products
   # slug = 'slug'
    

# def catalog(req, category_slug=None):

    # page = req.GET.get('page', 1)
    # on_sale = req.GET.get('on_sale', False)
    # order_by = req.GET.get('order_by', None)
    # query = req.GET.get('q', None)

    # if category_slug == 'all':
    #     goods = Products.objects.all()
    # elif query:
    #     goods = q_search(query)
    # else:
    #    goods = Products.objects.filter(category__slug=category_slug)
    #    if not goods.exists():
    #     raise Http404()

    # if on_sale:
    #     goods = goods.filter(discount__gt=0)

    # if order_by and order_by != 'default':
    #     goods = goods.order_by(order_by)

    # paginator = Paginator(goods, 3)
    # current_page = paginator.page(page)

#     context = {
#         'title': 'Home - Каталог',
#         'goods': current_page,
#         'slug_url': category_slug
#     }
#     return render(req, 'goods/catalog.html', context)

# def product(req, product_slug):
#     product = Products.objects.get(slug=product_slug)
#     context = {
#         'title': 'Home - Товар',
#         'product': product
#     }
#     return render(req, 'goods/product.html', context)