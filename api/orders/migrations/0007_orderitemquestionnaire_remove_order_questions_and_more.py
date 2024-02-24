# Generated by Django 4.2.10 on 2024-02-23 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_alter_orderitem_order_alter_orderitem_product_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItemQuestionnaire",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.CharField(max_length=255)),
                (
                    "order_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_item_questions",
                        to="orders.orderitem",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders_items",
                        to="orders.questionnaire",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="order",
            name="questions",
        ),
        migrations.DeleteModel(
            name="OrderQuestionnaire",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="questions",
            field=models.ManyToManyField(
                through="orders.OrderItemQuestionnaire", to="orders.questionnaire"
            ),
        ),
    ]