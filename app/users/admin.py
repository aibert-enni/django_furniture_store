from django.contrib import admin

from orders.admin import OrderTabAdmin
from carts.admin import CartTabAdmin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    inlines = [CartTabAdmin, OrderTabAdmin,]