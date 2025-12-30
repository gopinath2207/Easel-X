from django.contrib import admin
from .models import *
from Authentication.models import User
from .models import Artist, Product
from Core.models import Order

# Register your models here.
admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Product)
admin.site.register(Order)