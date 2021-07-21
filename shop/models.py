from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product},{self.quantity},{self.created_date}'

# switch customer to user so that we can use Django's componenents
# https://blog.crunchydata.com/blog/extending-djangos-user-model-with-onetoonefield 
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}, {self.customer.address}'

    class Meta:
        db_table = 'customer'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()

class LineItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey('shop.Cart', on_delete=models.CASCADE)
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product},{self.cart},{self.order},{self.created_date}'

class Order(models.Model):
    customer = models.ForeignKey('shop.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    # use decimal instead of float to avoid rounding errors
    # always use decimal for money values
    price = models.DecimalField(max_digits=4, decimal_places=2) 
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name},{self.price},{self.created_date}'


