from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True ,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    profile = models.ImageField(default="avatar1.png",null=True, blank = True)
    date_created = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    
    CATEGORY = (
        ("Desserts", "Desserts"), 
        ("Espresso", "Espresso"),
        ("Drinks","Drinks"),
        ("Wraps","Wraps"),
        ("cake", "Cake"),
        ("Specials","specials")
    )
    
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Ready', 'Ready'),
        ('Served', 'Served')
    )
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    Product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    
    