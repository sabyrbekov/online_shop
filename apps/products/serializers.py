from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.category.serializers import CategoryAPISerializer, BrandAPISerializer
from .models import ProductModel, Wish

User = get_user_model() 

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ('__all__')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = CategoryAPISerializer(instance=instance.category).data
        representation["brand"] = BrandAPISerializer(instance=instance.brand).data
        return representation



class WishAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('product', 'user')
