from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Customer, Order, Product
from .forms import ProductForm

# Create your views here.

def customer_list(request):
    users = User.objects.all()
    return render(request, 'shop/customer_list.html', {'users' : users})

def customer_detail(request, id):
    customer = get_object_or_404(Customer, id=customer.id)
    return render(request, 'shop/customer_detail.html', {'customer' : customer})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders' : orders})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'shop/order_detail.html', {'order' : order})

def product_list(request):
    products = Product.objects.all()
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = 'hello'
    
    return render(request, 'shop/product_list.html', {'products' : products, 'deleted': deleted })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product' : product})

def product_new(request):
    if request.method=="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()
    return render(request, 'shop/product_edit.html', {'form': form})

def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method=="POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_edit.html', {'form': form})

def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = product.name
    product.delete()
    return redirect('product_list' )
