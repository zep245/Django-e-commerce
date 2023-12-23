from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Category"
 
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
 
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=10 , blank=False)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default="")

    def save(self, *args, **kwargs):
        # Capitalize the color field before saving
        self.color = self.color.capitalize()
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Product"
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name
    

class ProductSize(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE , default="")
    size = models.CharField(max_length=6 , blank=False)

    class Meta:
        verbose_name_plural = "ProductSize"

    def __str__(self) -> str:
        return f"{self.category} - {self.size}"

    


    
    