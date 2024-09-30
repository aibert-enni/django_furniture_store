from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from carts.utils import get_user_carts
from carts.models import Cart
from goods.models import Products

def cart_add(req):
    
    product_id = req.POST.get('product_id')
    product = Products.objects.get(id=product_id)

    if req.user.is_authenticated:
        carts = Cart.objects.filter(user=req.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart(user=req.user, product=product, quantity=1).save()
    else:
        carts = Cart.objects.filter(session_key=req.session.session_key, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart( product=product, quantity=1, session_key=req.session.session_key).save()

    user_cart = get_user_carts(req)
        
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_cart}, request=req
    )

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html
    }

    return JsonResponse(response_data)

def cart_change(req):
    cart_id = req.POST.get('cart_id')
    quantity = req.POST.get('quantity')
    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_cart = get_user_carts(req)
        
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_cart}, request=req
    )

    response_data = {
        'message': 'Количества товара изменена',
        'cart_items_html': cart_items_html
    }
    
    return JsonResponse(response_data)

def cart_remove(req):
    cart_id = req.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(req)
        
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_cart}, request=req
    )

    response_data = {
        'message': 'Товар удален из корзины',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity
    }
    
    return JsonResponse(response_data)