from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter
from . import views

main_router = DefaultRouter()
main_router.register('collections', views.CollectionViewSet)

urlpatterns = [
    path('', include(main_router.urls))
]