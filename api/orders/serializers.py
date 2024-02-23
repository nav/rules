from rest_framework import serializers
from api.orders.models import Order, OrderItem
from api.rules.rules import RuleValidationMixin


class OrderItemSerializer(RuleValidationMixin, serializers.ModelSerializer):
    questionnaire = serializers.JSONField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ("product", "price", "questionnaire")


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("customer", "order_items")

    def create(self, validated_data):
        order_items = validated_data.pop("order_items")
        instance = super().create(validated_data)
        for item in order_items:
            item.pop("questionnaire")
            OrderItem.objects.create(order=instance, **item)
        return instance
