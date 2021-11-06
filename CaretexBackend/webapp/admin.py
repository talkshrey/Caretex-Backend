from django.contrib import admin
from django.contrib.admin.decorators import register
from . import models
from .models import Buyer, Outsider, Product, AllOrders

# Register your models here.
admin.site.register(Product)
admin.site.register(AllOrders)
admin.site.register(Buyer)
admin.site.register(Outsider)
