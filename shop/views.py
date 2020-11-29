from django.shortcuts import render, get_object_or_404
from .models import Customer, Order, Product

# Create your views here.
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'shop/customer_list.html', {'customers' : customers})

def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=id)
    return render(request, 'shop/customer_detail.html', {'customer' : customer})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders' : orders})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'shop/order_detail.html', {'order' : order})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products' : products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product' : product})