from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views

main_router = DefaultRouter()
main_router.register('collections', views.CollectionViewSet)
main_router.register('products', views.ProductViewSet)
main_router.register('carts', views.CartViewSet)
main_router.register('customer', views.CustomerViewSet)
main_router.register('orders', views.OrderViewSet, basename='orders')

product_review = NestedDefaultRouter(main_router, 'products', lookup='product')
product_review.register('reviews', views.ReviewViewSet,
                        basename='product-review')

cart_item = NestedDefaultRouter(main_router, 'carts', lookup='cart')
cart_item.register('items', views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(main_router.urls)),
    path('', include(product_review.urls)),
    path('', include(cart_item.urls))
]
