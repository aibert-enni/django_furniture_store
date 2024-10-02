from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('name', 'product',  'quantity', 'price',)
    readonly_fields = ('name', 'product')
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'name',  'quantity', 'price',)
    search_fields = ('order', 'name', 'product')

class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ('requires_delivery', 'status', 'payment_on_get', 'is_paid', 'created_timestamp',)
    readonly_fields = ('created_timestamp',)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'requires_delivery', 'payment_on_get', 'is_paid', 'created_timestamp',)
    list_filter = ('user', 'requires_delivery', 'payment_on_get', 'is_paid', 'status',)
    readonly_fields = ('created_timestamp',)
    search_fields = ('id',)
    inlines = [OrderItemTabAdmin,]