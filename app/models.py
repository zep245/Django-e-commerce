from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
class Sizes(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    size = models.CharField(max_length=5 , blank=True)
    
    class Meta:
        verbose_name_plural = 'Sizes'
    
    def __str__(self) -> str:
        return str(self.product)
    
    
class Colors(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    color = models.CharField(max_length=10 , blank=True)
    
    class Meta:
        verbose_name_plural = 'Colors'
    
    def __str__(self) -> str:
        return str(self.product)

    
    
    