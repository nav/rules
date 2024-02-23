from django.contrib import admin
from api.orders.models import Order, OrderItem, Product


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]


admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
