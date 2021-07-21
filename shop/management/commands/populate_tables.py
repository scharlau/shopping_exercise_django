"""
This file will populate the tables using Faker
"""
import random
import decimal
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
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
        User.objects.all().delete()
        print("tables dropped successfully")

        fake = Faker()

        # create some customers
        # we convert some values from tuples to strings
        for i in range(10):
            first_name = fake.first_name(),
            first_name = str(first_name[0])
            last_name = fake.last_name(),
            last_name = str(last_name[0])
            username = first_name + last_name,
            username = username[0]
            user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = fake.ascii_free_email(), 
            password = 'p@ssw0rd')
            customer = Customer.objects.get(user = user)
            customer.address = fake.address(),
            customer.address = str(customer.address[0])
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
            product = products[random_id],
            quantity = random.randrange(1,42),
            )
            cart.save()

        # create orders from customers
        customers = Customer.objects.all()
        for customer in customers:  
            for i in range(3):
                order = Order.objects.create(
                customer = customer,
                )
                order.save()
               
        # attach line_items to orders
        orders = Order.objects.all()
        carts = Cart.objects.all()
        for order in orders:
            for cart in carts:
                line_item = LineItem.objects.create(
                quantity = cart.quantity,
                product = cart.product,
                cart = cart,
                order = order,
                )
                line_item.save()
        
        print("tables successfully loaded")
               
    
