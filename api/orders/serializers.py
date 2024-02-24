from rest_framework import serializers
from api.orders.models import Order, OrderItem, OrderItemQuestionnaire
from api.rules.rules import RuleValidationMixin


class OrderItemQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemQuestionnaire
        fields = ("question", "answer")


class OrderItemSerializer(RuleValidationMixin, serializers.ModelSerializer):
    questions = OrderItemQuestionnaireSerializer(
        many=True,
        source="order_item_questions",
    )

    class Meta:
        model = OrderItem
        fields = ("product", "price", "questions")


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("customer", "order_items")

    def create(self, validated_data):
        order_items = validated_data.pop("order_items")

        instance = super().create(validated_data)

        for item in order_items:
            questions = item.pop("order_item_questions")
            order_item = OrderItem.objects.create(order=instance, **item)
            for question in questions:
                OrderItemQuestionnaire.objects.create(
                    order_item=order_item,
                    question=question["question"],
                    answer=question["answer"],
                )

        return instance
