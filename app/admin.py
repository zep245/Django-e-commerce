from django.contrib import admin
from .models import *

class AdminSize(admin.ModelAdmin):
    list_display = ['product' , 'size']

class AdminColor(admin.ModelAdmin):
    list_display = ['product' , 'color']


admin.site.register(Product)
admin.site.register(Sizes , AdminSize)
admin.site.register(Colors , AdminColor)