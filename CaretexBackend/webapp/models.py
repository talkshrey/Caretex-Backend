from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Buyer model - one who wants to buy products
class Buyer(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    address = models.TextField(max_length=500)
    pin = models.IntegerField()
    mobile = models.IntegerField()

# Seller models - one who is the seller and authorised to sell the product
class Product(models.Model):
    owner = models.ForeignKey(User, related_name='shopkeeper', on_delete=models.CASCADE)
    GTIN=models.BigIntegerField()
    code=models.CharField(max_length=25)
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=700)
    mrp=models.FloatField()
    quantity=models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Third party seller - one who is not authorised but still wants to sell a product
class Outsider(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    clientID = models.BigIntegerField(default=0)
    GTIN=models.BigIntegerField()
    code=models.CharField(max_length=25)
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=700)
    mrp=models.FloatField()
    quantity=models.IntegerField(default=0)
    

# Checkout model - model used while checking out and bill calculation 
class AllOrders(models.Model):
    amount=models.FloatField(default=0.00)
    product=models.ManyToManyField(Product)