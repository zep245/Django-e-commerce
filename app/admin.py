from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(Customers)
admin.site.register(Order)