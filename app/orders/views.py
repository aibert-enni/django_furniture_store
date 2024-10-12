from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from orders.services import PaymentProcessorFactory, StripePaymentProcessor, YOOKASSAPaymentProcessor
from orders.models import Order
from orders.utils import create_order
from orders.forms import CreateOrderForm

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        return create_order(self.request, form)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Home - Оформление заказа'
        context['order'] = True
        return context

class SuccessView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        paymentService = request.GET.get('service')
        if order_id:
            processor = PaymentProcessorFactory.get_processor(paymentService)
            
            paymentState = processor.handle_session(request)
            
            order = Order.objects.get(id=order_id)

            if paymentState:
                order.is_paid = True
                order.status = 'Оплачено'
                order.save()
            else:
                order.status = 'Неоплачено'
                order.save()
            
        return redirect('user:profile')
        

# @login_required
# def create_order(req):

#     if req.method == 'POST':
#         form = CreateOrderForm(req.POST)
#         if form.is_valid():
#             try:
#                 # Позволяет откатить транзакцию в случае ошибки, то есть если хоть один запрос вызовет ошибку, то все эти запросы не выполняться
#                 with transaction.atomic():
#                     user = req.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Создаем заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             requires_delivery=form.cleaned_data['requires_delivery'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )
#                         # Создаем заказанные товары
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.discount_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise Exception(f'Недостаточно количества товара {name} на складе\
#                                                 В наличии - {product.quantity} ')

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )

#                             product.quantity -= quantity
#                             product.save()

#                         # Очистка корзины
#                         cart_items.delete()
#                         messages.success(req, 'Заказ оформлен')
#                         return redirect('user:profile')
#             except ValidationError as e:
#                 messages.success(req, str(e))
#                 return redirect('cart:create_order')
#     else:
#         initial = {
#             'first_name': req.user.first_name,
#             'last_name': req.user.last_name,
#         }

#         form = CreateOrderForm(initial=initial)
    
#     context = {
#         'title': 'Home - Оформление заказа',
#         'order': True,
#         'form': form
#     }
#     return render(req, 'orders/create_order.html', context)