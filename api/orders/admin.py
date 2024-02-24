import json
from django import forms
from django.contrib import admin
from api.orders.models import (
    Order,
    OrderItem,
    OrderItemQuestionnaire,
    Product,
    Questionnaire,
)


class PrettyJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


class OrderItemQuestionnaireAdmin(admin.TabularInline):
    model = OrderItemQuestionnaire


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    inlines = [OrderItemQuestionnaireAdmin]


class OrderAdmin(admin.ModelAdmin):
    model = Order


class ProductForm(forms.ModelForm):
    metadata = forms.JSONField(encoder=PrettyJSONEncoder)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    form = ProductForm


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Questionnaire)
