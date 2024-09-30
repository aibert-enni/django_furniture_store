from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import Cart
from users.models import User
from goods.models import Products

def cart_add(req, product_slug):
    product = Products.objects.get(slug=product_slug)

    if req.user.is_authenticated:
        carts = Cart.objects.filter(user=req.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart(user=req.user, product=product, quantity=1).save()
    # else:
    #     carts = Cart.objects.filter(session_key=req.session.session_key, product=product)
    #     if cart.exists():
    #         cart = carts.first()
    #         if cart:
    #             cart.quantity += 1
    #             cart.save()
    #     else:
    #         Cart( product=product, quantity=1, session_key = req.session.session.key).save()
        
    return redirect(req.META['HTTP_REFERER'])

def cart_change(req, product_slug):
    ...

def cart_remove(req, product_slug):
    ...