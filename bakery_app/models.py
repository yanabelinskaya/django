from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib import admin

class Bakery(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    products_link = models.URLField()

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('bread', 'Хлеб'),
        ('buns', 'Булочки'),
        ('cakes', 'Торты'),
        ('pastries', 'Пирожные'),
        ('croissants', 'Круассаны'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

from django.contrib.auth.hashers import check_password

class Customer(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    deliveries = models.ManyToManyField('Delivery', related_name='customers')


    # Переопределим save(), чтобы автоматизировать присвоение значения username
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Присваиваем email значению username, если оно пустое
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
    @property
    def latest_delivery(self):
        return self.delivery_set.last()
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField(null=True, blank=True)  # Адрес доставки

    def __str__(self):
        return f'Order {self.id} by {self.customer}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'
    
    @property
    def total_price(self):
        return self.quantity * self.price



class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='delivery_set')
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    delivery_address = models.TextField()

    def __str__(self):
        return f'Доставка для заказа {self.order.id}'

    
class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.name} ({self.quantity} шт.)'
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
