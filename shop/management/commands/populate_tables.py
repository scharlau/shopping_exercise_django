"""
This file will populate the tables using Faker
"""
import random
import decimal
from datetime import datetime
from django.db import models
from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from shop.models import Cart, Customer, LineItem, Order, Product

class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):

# drop the tables - use this order due to foreign keys - so that we can rerun the file as needed without repeating values
        Cart.objects.all().delete()
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        print("tables dropped successfully")

        fake = Faker()

        # create some customers
        for i in range(10):
            customer = Customer.objects.create(
            name = fake.name(),
            email = fake.ascii_free_email(),
            address = fake.address(),
            )
            customer.save()

        # create some products
        for i in range(10):
            product = Product.objects.create(
            name = fake.catch_phrase(),
            price = int( decimal.Decimal(random.randrange(155,899))/100),
            )
            product.save()

        # create some carts 
        products = list(Product.objects.all())
        for i in range(10):
            random_id = random.randint(1,9)
            cart = Cart.objects.create(
            product_id = products[random_id],
            quantity = random.randrange(1,42),
            )
            cart.save()

        # create orders from customers
        customers = Customer.objects.all()
        for customer in customers:  
            for i in range(3):
                order = Order.objects.create(
                customer_id = customer,
                )
                order.save()
               
        # attach line_items to orders
        orders = Order.objects.all()
        carts = Cart.objects.all()
        for order in orders:
            for cart in carts:
                line_item = LineItem.objects.create(
                quantity = cart.quantity,
                product_id = cart.product_id,
                cart_id = cart,
                order_id = order,
                )
                line_item.save()
        
        print("tables successfully loaded")
               
    
