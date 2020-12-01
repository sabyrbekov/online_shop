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



# class WishAPISerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Wish
#         fields = ('product', 'user')

class BucketlistItemSerializer(serializers.ModelSerializer):
    """
    Serialier class for a bucketlist item
    """

    def create(self, validated_data):
        try:
            if not validated_data.get('item_name'):
                raise serializers.ValidationError('The name cannot be empty')
            return super(BucketlistItemSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    def update(self, instance, validated_data):
        try:
            return super(BucketlistItemSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    class Meta:
        model = BucketlistItem
        fields = ('id', 'item_name', 'date_created', 'date_modified', 'is_done')
        read_only_fields = ('id', 'date_created', 'date_modified')


class BucketlistSerializer(serializers.ModelSerializer):
    """
    serializer class for bucketlists
    """
    bucketlist_items = BucketlistItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        try:
            if not validated_data.get('name'):
                raise serializers.ValidationError('The name cannot be empty')
            return super(BucketlistSerializer, self).create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    def update(self, instance, validated_data):
        try:
            return super(BucketlistSerializer, self).update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError('That name already exists')

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'description', 'date_created', 'date_modified', 'bucketlist_items')
        read_only_fields = ('id', 'date_created', 'date_modified','created_by', 'bucketlist_items')
