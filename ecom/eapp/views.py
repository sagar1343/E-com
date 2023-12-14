from django.shortcuts import render
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    category = Category.objects.all()
    return render(request, template_name="home.html", context={'products': products, 'category': category})


def fliter(request, category_id):
    category = Category.objects.all()
    filter_product = Product.objects.filter(category=category_id)
    return render(request, template_name="home.html", context={'products': filter_product,'category': category})


def store(request):
    return render(request, template_name="store.html")


def account(request):
    return render(request, template_name="account.html")
