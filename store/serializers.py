from rest_framework import serializers
from .models import Collection, Product, Review, Cart, CartItem, Customer, Order, OrderItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description',
                  'unit_price', 'last_update', 'collection', 'promotion']


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'product_id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total']
    

    total = serializers.SerializerMethodField(method_name='calculate_total')

    def calculate_total(self, cartitem: CartItem):
        return cartitem.product.unit_price * cartitem.quantity

    


class SimpleCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does't exists.")
        else:
            return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']

        try:
            cartitem_obj = CartItem.objects.get(
                product_id=product_id, cart_id=cart_id)
            cartitem_obj.quantity += quantity
            cartitem_obj.save()

            self.instance = cartitem_obj
        except CartItem.DoesNotExist:
            cartitem_obj = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
            self.instance = cartitem_obj
        return self.instance


class CartSerializer(serializers.ModelSerializer):

    cartitem = CartItemSerializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'cartitem', 'total']

    total = serializers.SerializerMethodField(method_name='calculate_total')

    def calculate_total(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.cartitem.all()])
    
class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'membership']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = ['id', 'customer', 'palce_at', 'payment_status']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderItem
        fields = ['id', 'quantity', 'unit_price', 'order_id', 'product']
