from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def customer_list(request):
    users = User.objects.all()
    return render(request, 'shop/customer_list.html', {'users' : users})

def customer_detail(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'shop/customer_detail.html', {'user' : user})

