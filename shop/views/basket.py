from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from shop.forms import BasketAddProductForm 

class Basket(object):
    # a data transfer object to shift items from cart to page
    # inspired by Django 3 by Example (2020) by Antonio Mele
    # https://github.com/PacktPublishing/Django-3-by-Example/
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty basket in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __iter__(self):
        """
        Iterate over the items in the basket and get the products
        from the database.
        """
        print(f'basket: { self.basket }')
        product_ids = self.basket.keys()
        # get the product objects and add them to the basket
        products = Product.objects.filter(id__in=product_ids)

        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
            basket[str(product.id)]['product_id'] = product.id

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the basket.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the basket or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the basket.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())


@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('shop:basket_detail')

@require_POST
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect('shop:basket_detail')

def basket_detail(request):
    basket = Basket(request)
    for item in basket:
        item['update_quantity_form'] = BasketAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'shop/basket.html', {'basket': basket})
