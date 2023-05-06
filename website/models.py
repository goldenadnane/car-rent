from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Year(models.Model):
    name = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    year_id = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
    about = models.TextField(max_length=355, null=True, blank=True)
    model = models.CharField(max_length=70, null=True, blank=True)
    topSpeed = models.IntegerField(null=True, blank=True)
    nm = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=10, null=True, blank=True)
    available_choices = (
        ("AVAILAIBLE", "Available"),
        ("NOT_AVAILABLE", "Not_Available"),
    )
    available = models.CharField(
        max_length=14, choices=available_choices, default="")
    car1 = models.ImageField(null=True, default="static/placeholder.png")
    car2 = models.ImageField(null=True, default="static/placeholder.png")
    car3 = models.ImageField(null=True, default="static/placeholder.png")

    def __str__(self):
        return self.model


class Faq(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.TextField(max_length=375, null=True, blank=True)
    question = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    cne = models.CharField(max_length=50, null=True)
    full_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.CharField(max_length=25, null=True)
    adresse = models.CharField(max_length=50, null=True)
    profilePic = models.ImageField(
        default="basicUser.jpg", null=True, blank=True)

    def __str__(self):
        return self.full_name


class Order(models.Model):

    customer = models.CharField(max_length=30,null=False)
    customerID = models.IntegerField(null=False)
    model = models.CharField(max_length=70, null=True)
    automobileId = models.IntegerField(null=False)
    price = models.IntegerField(null=True, blank=False)
    startRent = models.DateField(auto_now_add=False, null=True)
    endRent = models.DateField(auto_now_add=False, null=True)
    orderDate = models.DateTimeField(auto_now_add=True, null=True)
    payed = models.BooleanField(null=True, default=False)

    def __int__(self):
        return self.id


class canceledOrders(models.Model):
    customerID = models.IntegerField(null=False)
    automobileId = models.IntegerField(null=False)
    price = models.IntegerField(null=True, blank=False)
    payed = models.BooleanField(null=True, default=False)
