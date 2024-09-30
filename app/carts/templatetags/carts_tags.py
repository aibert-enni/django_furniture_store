from django import template

from carts.models import Cart


register = template.Library()

@register.simple_tag()
def user_carts(req):
    if req.user.is_authenticated:
        return Cart.objects.filter(user=req.user)
    
    return None

