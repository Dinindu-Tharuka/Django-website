from rest_framework import serializers
from .models import Collection, Product, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'last_update', 'collection', 'promotion']

class ReviewSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(read_only=True)

    class Meta:
        model= Review
        fields = ['id', 'product_id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)