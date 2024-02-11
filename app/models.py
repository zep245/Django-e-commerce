from django.db import models
from django.contrib.auth.hashers import make_password

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default="", null=True)

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



class Customers(models.Model):
    email = models.EmailField(unique=True , blank=False)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(blank=True, null=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Customers"

    @classmethod
    def get_customer_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def get_otp_expiry_time(self):
        return self.otp_expiry_time

    def get_otp(self):
        return self.otp

    def __str__(self):
        return self.email


class Order(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, blank=False, null=False, default="")
    size = models.CharField(max_length=10, blank=False, null=False, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False  , default=0)
    quantity = models.CharField(max_length=10, blank=False, null=False, default="")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False , default=0)
    email = models.EmailField(blank=False, null=False)
    phone_number = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=30, blank=False, null=False)
    first_name = models.CharField(max_length=40, blank=False, null=False)
    last_name = models.CharField(max_length=40, blank=False, null=False)
    city = models.CharField(max_length=40, blank=False, null=False)
    state = models.CharField(max_length=40, blank=False, null=False)
    pincode = models.CharField(max_length=40, blank=False, null=False)
    payment_type = models.CharField(max_length=40, blank=False, null=False)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Order"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.customer} Ordered {self.product}"



    
    