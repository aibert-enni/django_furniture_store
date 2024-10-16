from decimal import Decimal
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.shortcuts import redirect

from orders.services import PaymentProcessorFactory
from carts.models import Cart
from orders.models import Order, OrderItem


def create_order(req, form):
            try:
                # Позволяет откатить транзакцию в случае ошибки, то есть если хоть один запрос вызовет ошибку, то все эти запросы не выполняться
                with transaction.atomic():
                    user = req.user
                    cart_items = Cart.objects.filter(user=user)
                    amount = 0

                    if cart_items.exists():
                        # Создаем заказ
                        payment_type = form.cleaned_data['payment_on_get']
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get = payment_type=='on_get' if True else False,
                        )
                        # Создаем заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.discount_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise Exception(f'Недостаточно количества товара {name} на складе\
                                                В наличии - {product.quantity} ')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()
                        amount = cart_items.total_price()
                        # Очистка корзины
                        cart_items.delete()
                        
                        if payment_type != 'on_get':
                            processor = PaymentProcessorFactory.get_processor(payment_type)
                            match payment_type:
                                case 'stripe':
                                    url = processor.create_chechout_session(f'Заказ № {order.id}', int(amount * 100), 'usd', f'orders/success/?order_id={order.id}', 'user/profile')
                                case 'yookassa':
                                    url = processor.create_chechout_session(req, f'Заказ № {order.id}', round(amount * Decimal(95.68), 2), 'RUB', f'orders/success/?order_id={order.id}')
                            return redirect(url)
                        messages.success(req, 'Заказ оформлен')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(req, str(e))
                return redirect('cart:create_order')
    