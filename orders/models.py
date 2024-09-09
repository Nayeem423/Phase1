# models.py in the orders app

from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

class Order(models.Model):
    client_name = models.CharField(max_length=100)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=50, default='Pending')
    products = models.ManyToManyField(Product, through='OrderProduct')

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=50, default='Not Delivered')
    delivery_date = models.DateTimeField(null=True, blank=True)

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)  # e.g., 'Advance', 'Refund', 'Discount'
    date = models.DateTimeField(auto_now_add=True)
