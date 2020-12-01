from rest_framework import serializers

from .models import Category, Brand

class CategoryAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'title'
        )
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategoryAPISerializer(
                instance.children.all(), many=True
            ).data

        return representation

class BrandAPISerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'title', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
        

            

