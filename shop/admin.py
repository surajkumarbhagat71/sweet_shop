from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Sweets)
admin.site.register(AddToCart)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Owner)