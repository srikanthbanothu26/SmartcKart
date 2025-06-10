from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=300)
    cost_price = models.FloatField()
    sales_price = models.FloatField()
    display_name = models.CharField(max_length=400)
    image = models.ImageField(upload_to='product_img/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    barcode = models.CharField(max_length=20, blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=20, blank=True, null=True)
    avail_qty = models.IntegerField(default=1)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.display_name


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    status = models.BooleanField(default=False)
    qty = models.IntegerField(blank=True, null=True)
    payment = models.FloatField(default=0)
    payment_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='draft')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.product.name


class wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.product.name


class Payments(models.Model):
    payment_method = [
        ('upi', 'UPI'),
        ('debit_card', 'Debit Card'),
        ('phonepe', 'PhonePe'),
        ('gpay', 'GPay'),
        ('net_banking', 'Net Banking'),
        ('cod', 'Cash on Delivery')
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    payment_type = models.CharField(max_length=100, choices=payment_method, default='upi')
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.id
