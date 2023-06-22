from django.contrib import admin
from .models import Collection, Product, Customer


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'membership']
    list_select_related = ['user']

    def first_name(self, customer):
        return customer.user.first_name
    
    def last_name(self, customer):
        return customer.user.last_name
