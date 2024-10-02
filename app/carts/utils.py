from collections import defaultdict
from carts.models import Cart
from django.db.models import Count

def get_user_carts(req):
    if req.user.is_authenticated:
        return Cart.objects.filter(user=req.user).select_related('product')
    
    if not req.session.session_key:
        req.session.create()
    
    return Cart.objects.filter(session_key=req.session.session_key).select_related('product')
            
def delete_carts_duplicates(user, carts):
    duplicates = (
        Cart.objects
        .filter(user=user)  # Фильтруем по пользователю
        .values('product')  # Группируем по продукту
        .annotate(count=Count('id'))  # Подсчитываем количество записей
        .filter(count__gt=1)  # Оставляем только те группы, где больше 1 записи
    )

    if not duplicates.exists():
        return

    duplicates_map = defaultdict(list)

    for cart in carts:
        duplicates_map[cart.product].append(cart)

    # Удаляем дубликаты, оставляя только одну запись для каждого продукта
    for product, duplicates in duplicates_map.items():
        for record in duplicates[1:]:
            record.delete()