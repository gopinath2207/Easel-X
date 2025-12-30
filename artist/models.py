from django.db import models
from Authentication.models import User
import os
# Create your models here.

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=None)
    profile_picture = models.ImageField(
        upload_to='artist_profiles/', 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    insta = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_profile_picture_url(self):
        """
        Returns the URL of the profile picture if it exists,
        otherwise returns the default profile picture URL
        """
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/default_profile.png'
    
class Product(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artist_products/')
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    medium = models.CharField(max_length=100)
    year_created = models.PositiveIntegerField()
    description = models.TextField()
    # Dimensions could be stored 
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text="Width in inches")
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text="Height in inches")
    depth = models.DecimalField(max_digits=6, decimal_places=2, help_text="Depth in inches", blank=True, null=True)
    # is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    tags_keywords = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated tags/keywords")
    framed = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    certificate_of_authenticity = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title