from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from .models import Collection, Product, OrderItem, Review, Cart, CartItem
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, SimpleCartItemSerializer
from .pagination import DefaultPagination


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(product_id=self.kwargs['product_pk'])
        return queryset

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }


class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SimpleCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
        return queryset

    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }
