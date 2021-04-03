from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cart, Customer, LineItem, Order, Product
from .forms import ProductForm, SignUpForm


class Basket:
    # a data transfer object to shift items from cart to page
    
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

# Create your views here.

# convenience method as used in several methods
def get_basket(request):
    basket = request.session.get('basket', [])
    products = []
    for item in basket:
        product = Product.objects.get(id=item[0])
        basket = Basket(item[0], product.name, product.price, item[1])
        products.append(basket)
    return products

def basket(request):
    products = get_basket(request)
    return render(request, 'shop/basket.html', {'products': products})

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.customer.address = form.cleaned_data.get('address')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password= password)
        login(request, user)
        return redirect('/')
    return render(request, 'signup.html', {'form': form})

def customer_list(request):
    users = User.objects.all()
    return render(request, 'shop/customer_list.html', {'users' : users})

def customer_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'shop/customer_detail.html', {'user' : user})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders' : orders})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'shop/order_detail.html', {'order' : order})

# save order, clear basket and thank customer
def payment(request):
    products = get_basket(request)
    user = request.user
    order = Order.objects.create(customer=user.customer)
    order.refresh_from_db()
    for product in products:
        product_item = get_object_or_404(Product, id=product.id)
        cart = Cart.objects.create(product = product_item, quantity=product.quantity)
        cart.refresh_from_db()
        line_iten = LineItem.objects.create(quantity=product.quantity, product=product_item, 
        cart=cart,  order = order)

    request.session['basket'].clear()
    request.session['deleted'] = 'thanks for your purchase'
    return redirect('product_list' )

def product_buy(request):
    if request.method== "POST":
        temp_id = int(request.POST.get('id',''))
        quantity = int(request.POST.get('quantity', ''))
        basket = request.session['basket']
        basket.append([temp_id,quantity])
        request.session['basket'] = basket
    return redirect('product_list')

def product_list(request):
    products = Product.objects.all()
    basket = request.session.get('basket', [])
    request.session['basket'] = basket 
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

def purchase(request):
    user = request.user
    products = get_basket(request)
    total = 0
    for product in products:
        total += product.price * product.quantity
    return render(request, 'shop/purchase.html', {'products': products, 'user': user, 'total': total})
