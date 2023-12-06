from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .models import Collection, Product, OrderItem, Review, Cart, CartItem, Customer, Order, ProductImages
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, SimpleCartItemSerializer, CustomerSerializer, OrderSerializer
from .serializers import OrderCreateSerializer, UpdateOrderSerializer, ProductImageSerilaizer
from .pagination import DefaultPagination
from .permission import IsAdminOrReadOnly


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerilaizer

    def get_queryset(self):
        return ProductImages.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {
            'product_id':self.kwargs['product_pk']
        }


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(product_id=self.kwargs['product_pk'])
        return queryset

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }


class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('cartitem__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return SimpleCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(
            cart_id=self.kwargs['cart_pk']).select_related('product')
        return queryset

    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer, isAvailable = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['patch', 'get', 'post', 'delete', 'head', 'options'] 

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data, 
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        if self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()

        (customer_id, created) = Customer.objects.only(
            'id').get_or_create(id=self.request.user.id)
        return Order.objects.filter(customer_id=customer_id)
