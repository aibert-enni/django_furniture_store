from abc import ABC, abstractmethod
import uuid

from django.forms import ValidationError
from django.conf import settings

import stripe
from yookassa import Payment, Configuration



class PaymentProcessor(ABC):
    @abstractmethod
    def create_chechout_session(self,*args, **kwargs):
        pass

    @abstractmethod
    def handle_session(request):
        pass


class StripePaymentProcessor(PaymentProcessor):
    _domain = settings.DOMAIN
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    @classmethod
    def create_chechout_session(cls, name, amount, currency, success_url, cancel_url):
        print(settings.STRIPE_SECRET_KEY)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': currency,
                            'unit_amount': amount,
                            'product_data': {
                                'name': name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'{cls._domain}/{success_url}&service=stripe' + '&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=f'{cls._domain}/{cancel_url}',
            )
            return checkout_session.url
        except Exception as e:
            raise ValidationError(f"Ошибка при создании сессии: {str(e)}")

    @staticmethod
    def handle_session(request):
        session_id = request.GET.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)
        if session['payment_status'] == 'paid':
            return True
        else:
            return False
        

class YOOKASSAPaymentProcessor(PaymentProcessor):
    _domain = settings.DOMAIN
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    Configuration.account_id = settings.YOOKASSA_SHOP_ID

    @classmethod
    def create_chechout_session(cls, request, name, amount, currency, success_url):
        try:
            indempotence_key = str(uuid.uuid4())
            payment = Payment.create({
                "amount": {
                    "value": str(amount),
                    "currency": currency
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"{cls._domain}/{success_url}&service=yookassa"
                },
                "capture": True,
                "test": True,
                "description": name
            },
            indempotence_key)
            request.session['yookassa_payment_id'] = payment.id
            return payment.confirmation.confirmation_url
        except Exception as e:
            raise ValidationError(f"Ошибка при создании сессии: {str(e)}")

    @staticmethod
    def handle_session(request):
        payment_id = request.session.get('yookassa_payment_id')
        if payment_id:
            del request.session['yookassa_payment_id']
        payment = Payment.find_one(payment_id)
        if payment.status == 'succeeded':
            return True
        else:
            return False
    
class PaymentProcessorFactory:
    @staticmethod
    def get_processor(paymentService):
        match paymentService:
            case 'stripe':
                return StripePaymentProcessor
            case 'yookassa':
                return YOOKASSAPaymentProcessor
            case _:
                raise ValidationError("Неизвестный сервис оплаты")