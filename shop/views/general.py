from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from shop.models import Cart, Customer, LineItem, Order, Product
from shop.forms import SignUpForm
from shop.views import Basket

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

# save order, clear basket and thank customer
def payment(request):
    basket = Basket(request)
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.id)
    order = Order.objects.create(customer=customer)
    order.refresh_from_db()
    for item in basket:
        product_item = get_object_or_404(Product, id=item['product_id'])
        cart = Cart.objects.create(product = product_item, quantity=item['quantity'])
        cart.refresh_from_db()
        line_item = LineItem.objects.create(quantity=item['quantity'], product=product_item, cart=cart,  order = order)

    basket.clear()
    request.session['deleted'] = 'thanks for your purchase'
    return redirect('shop:product_list' )

def purchase(request):
    if request.user.is_authenticated:
       user = request.user
       basket = Basket(request)
       
       return render(request, 'shop/purchase.html', {'basket': basket, 'user': user})
    else:
        return redirect('login')