from urllib import request
from django.db import models
# from django.contrib.auth.models import User
from Authentication.models import User
from django.utils import timezone
from artist.models import Artist as ArtistProfile, Product
# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('SHIPPING', 'Shipping'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(ArtistProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=30, default=None)
    lastName = models.CharField(max_length=30, default=None)
    email = models.EmailField(default=None)
    phone = models.CharField(max_length=15, default=None)
    address = models.TextField(default=None)
    city = models.CharField(max_length=100, default=None)
    state = models.CharField(max_length=100, default=None)
    postal_code = models.IntegerField(default=None)
    country = models.CharField(max_length=100, default=None)
    order_date = models.DateTimeField(default=timezone.now)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROCESSING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    #transaction details
    card_no = models.CharField(max_length=19)
    card_expiry = models.CharField(max_length=5)  # MM/YY format
    card_cvv = models.CharField(max_length=4)
    card_holder = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"