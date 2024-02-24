from django.db import models


class Questionnaire(models.Model):
    slug = models.SlugField()
    question = models.TextField(max_length=255)

    def __str__(self):
        question_headline = self.question.split("\n")[0]
        return f"Question: {question_headline}"


class Product(models.Model):
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Questionnaire)
    metadata = models.JSONField()

    def __str__(self):
        return f"Product: {self.sku}"


class Order(models.Model):
    customer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items = models.ManyToManyField(Product, through="OrderItem")

    def __str__(self):
        return f"Order: {self.pk} {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    questions = models.ManyToManyField(Questionnaire, through="OrderItemQuestionnaire")

    def __str__(self):
        return f"OrderItem: {self.pk} {self.order_id}"


class OrderItemQuestionnaire(models.Model):
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name="order_item_questions"
    )
    question = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, related_name="orders_items"
    )
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"OrderItemQuestionnaire: {self.pk} {self.order_item} {self.question}"
