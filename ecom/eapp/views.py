from django.shortcuts import render

from .models import Product, Category


def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request, template_name="home.html", context={'products': products, 'category': category})


def store(request):
    return render(request, template_name="store.html")


def account(request):
    return render(request, template_name="account.html")
