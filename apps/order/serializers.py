
from rest_framework import serializers

from .models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'address', 'city', 'product'
    ]