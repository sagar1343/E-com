from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.home, name='eapp-home'),
    path("store", views.store, name='eapp-store'),
    path("account", views.account, name='eapp-account')
]
