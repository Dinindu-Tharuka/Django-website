from django.contrib import admin
from .models import Collection, Product, Customer, ProductImages
from django.utils.html import format_html


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title']

class ProductImage(admin.TabularInline):
    model = ProductImages
    readonly_fields = ['thumbnail']

    def thumbnail(self, insatnce):
        if insatnce.image.name:
            return format_html(f'<img src="{insatnce.image.url}" class="thumbnail"/>')
        return ''

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price']
    inlines = [ProductImage]

    class Media:
        css = {
            'all':['store/styles.css']
        }

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'membership']
    list_select_related = ['user']

    def first_name(self, customer):
        return customer.user.first_name
    
    def last_name(self, customer):
        return customer.user.last_name
