from django.db import models
from django.conf import settings
from uuid import uuid4


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self) -> str:
        return self.description


class Collection(models.Model):
    title = models.CharField(max_length=255)

    ###
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='product')
    promotion = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title


class Customer(models.Model):

    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_BRONZ = 'B'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_BRONZ, 'Bronz')
    ]

    phone = models.CharField(max_length=255)
    birthdate = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZ)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Order(models.Model):

    STATUS_PENDING = 'P'
    STATUS_COMPLETE = 'C'
    STATUS_FAILED = 'F'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'PENDING'),
        (STATUS_COMPLETE, 'COMPLETE'),
        (STATUS_FAILED, 'FAILED')
    ]

    palce_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)

    ###
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='order')


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    ###
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='orderitem')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitem')


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    palce_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    quantity = models.IntegerField()
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitem')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='cartitem')


class Review(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='review')
