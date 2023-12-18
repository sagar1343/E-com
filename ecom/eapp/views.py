from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect

from .models import Product, Category, CartItem


def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    cart_item = CartItem.objects.all()
    total_quantity = CartItem.objects.aggregate(Sum("quantity"))
    return render(request, template_name="home.html",
                  context={'products': products, 'category': category, 'cart_item': cart_item,
                           'total_quantity': total_quantity})


def fliter(request, category_id):
    category = Category.objects.all()
    filter_product = Product.objects.filter(category=category_id)
    total_quantity = CartItem.objects.aggregate(Sum("quantity"))
    return render(request, template_name="home.html",
                  context={'products': filter_product, 'category': category, 'total_quantity': total_quantity})


def store(request):
    cart_item = CartItem.objects.all()
    total_quantity = CartItem.objects.aggregate(Sum("quantity"))
    total_price = sum(item.item_total() for item in cart_item)
    return render(request, template_name="store.html",
                  context={'cart_item': cart_item, 'total_quantity': total_quantity, 'total_price': total_price})


def account(request):
    user = User.objects.all()
    total_quantity = CartItem.objects.aggregate(Sum("quantity"))
    return render(request, template_name="account.html", context={'User': user, 'total_quantity': total_quantity})


def clear(request):
    cart_item = CartItem.objects.all()
    cart_item.delete()
    return render(request, template_name="store.html", context={'cart_item': cart_item})


def clear_one(request, product_id):
    del_cart_item = CartItem.objects.get(pk=product_id)
    del_cart_item.delete()
    cart_item = CartItem.objects.all()
    return redirect(to='eapp-store')


def add_product_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.filter(item_name=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        new_cart_item = CartItem(item_name=product, quantity=1)
        new_cart_item.save()
    return redirect(to='eapp-home')


def increment_quantity(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.filter(item_name=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    return redirect(to='eapp-store')


def decrement_quantity(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.filter(item_name=product).first()
    if cart_item:
        cart_item.quantity = max(1, cart_item.quantity - 1)
        cart_item.save()
    return redirect(to='eapp-store')
