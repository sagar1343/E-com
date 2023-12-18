from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='eapp-home'),
    path("store", views.store, name='eapp-store'),
    path("account", views.account, name='eapp-account'),
    path("filter/<int:category_id>/", views.fliter, name='eapp-filter'),
    path("clear/", views.clear, name='eapp-clear'),
    path("clear_one/<int:product_id>", views.clear_one, name='eapp-clear-one'),
    path("addtocart/<int:product_id>", views.add_product_to_cart, name='eapp-add'),
    path("increment/<int:product_id>", views.increment_quantity, name='eapp-incre'),
    path("decrement/<int:product_id>", views.decrement_quantity, name='eapp-decre')
]
