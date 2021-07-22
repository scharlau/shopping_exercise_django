from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from shop.models import Cart, LineItem, Order, Product
from shop.forms import SignUpForm


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

@login_required
def dashboard(request):
    user = request.user
    if user.is_authenticated & user.is_staff:
        return render(request, 'shop/dashboard.html')
    else:
        return redirect('/accounts/login.html')

def product_buy(request):
    if request.method== "POST":
        temp_id = int(request.POST.get('id',''))
        quantity = int(request.POST.get('quantity', ''))
        basket = request.session['basket']
        basket.append([temp_id,quantity])
        request.session['basket'] = basket
    return redirect('product_list')

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

def purchase(request):
    if request.user.is_authenticated:
       user = request.user
       products = get_basket(request)
       total = 0
       for product in products:
           total += product.price * product.quantity
       return render(request, 'shop/purchase.html', {'products': products, 'user': user, 'total': total})
    else:
        return redirect('login')