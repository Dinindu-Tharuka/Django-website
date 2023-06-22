from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views

main_router = DefaultRouter()
main_router.register('collections', views.CollectionViewSet)
main_router.register('products', views.ProductViewSet)

product_review = NestedDefaultRouter(main_router, 'products', lookup='product')
product_review.register('reviews', views.ReviewViewSet, basename='product-review')

urlpatterns = [
    path('', include(main_router.urls)),
    path('', include(product_review.urls)),
]