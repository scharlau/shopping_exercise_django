from django.db import models
from django.utils import timezone

# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id},{self.quantity},{self.created_date}'

class Customer(models.Model):
    name = models.TextField()
    email = models.TextField()
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name},{self.email},{self.address},{self.created_date}'

class LineItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey('shop.Cart', on_delete=models.CASCADE)
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product_id},{self.cart_id},{self.order_id},{self.created_date}'

class Order(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer_id},{self.created_date}'

class Product(models.Model):
    name = models.TextField()
    price = models.FloatField() 
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name},{self.price},{self.created_date}'
