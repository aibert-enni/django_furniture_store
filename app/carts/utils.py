from carts.models import Cart


def get_user_carts(req):
    if req.user.is_authenticated:
        return Cart.objects.filter(user=req.user)