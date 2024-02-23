from rest_framework import viewsets
from api.orders.serializers import OrderSerializer
from api.orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
