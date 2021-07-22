from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from shop.models import LineItem, Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders' : orders})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)
    line_items = LineItem.objects.filter(order_id=order.id)
    return render(request, 'shop/order_detail.html', {'order' : order, 'user': user, 'line_items': line_items})
