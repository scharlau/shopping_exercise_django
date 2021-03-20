from django.urls import path
from . import views

# the empty path '' becomes the 'home page
urlpatterns = [
        path('', views.customer_list, name='customer_list'),
        path('customer/<int:id>/', views.customer_detail, name= 'customer_detail'),
        path('order_list', views.order_list, name='order_list'),
        path('order/<int:id>/', views.order_detail, name= 'order_detail'),
        path('product_list', views.product_list, name='product_list'),
        path('product/<int:id>/', views.product_detail, name= 'product_detail'),
        path('product_new/', views.product_new, name= 'product_new'),
        path('product/<int:id>/edit/', views.product_edit, name= 'product_edit'),
        path('product/<int:id>/delete/', views.product_delete, name= 'product_delete'),
        ]