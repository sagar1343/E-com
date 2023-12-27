from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, CartItem
from django.contrib.auth.forms import UserCreationForm


def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    total_quantity = cart_item.aggregate(Sum("quantity"))
    return render(request, template_name="home.html",
                  context={'products': products, 'category': category, 'cart_item': cart_item,
                           'total_quantity': total_quantity})


def fliter(request, category_id):
    category = Category.objects.all()
    filter_product = Product.objects.filter(category=category_id)
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    total_quantity = cart_item.aggregate(Sum("quantity"))
    return render(request, template_name="home.html",
                  context={'products': filter_product, 'category': category, 'total_quantity': total_quantity})


def account(request):
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    total_quantity = cart_item.aggregate(Sum("quantity"))
    return render(request, template_name='account.html', context={'total_quantity': total_quantity})


@login_required
def store(request):
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    total_quantity = cart_item.aggregate(Sum("quantity"))
    total_price = sum(item.item_total() for item in cart_item)
    return render(request, template_name="store.html",
                  context={'cart_item': cart_item, 'total_quantity': total_quantity, 'total_price': total_price})


@login_required
def clear(request):
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    cart_item.delete()
    return render(request, template_name="store.html", context={'cart_item': cart_item})


@login_required
def clear_one(request, product_id):
    cart_item = CartItem.objects.filter(customer_id=request.user.id)
    del_cart_item = cart_item.get(pk=product_id)
    del_cart_item.delete()
    messages.success(request, f"{del_cart_item.item_name} removed from the cart")
    return redirect(to='eapp-store')


@login_required
def add_product_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(pk=product_id)
    cart = CartItem.objects.filter(customer=user)
    cart_item = cart.filter(item_name=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        new_cart_item = CartItem(item_name=product, quantity=1, customer=user)
        new_cart_item.save()
    messages.success(request, f"{product.name} added to the cart")
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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            return redirect(to='login')
    else:
        form = UserCreationForm()
    return render(request, template_name='register.html', context={'form': form})
