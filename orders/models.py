from django.db import models
from common.models import BaseModel
from users.models import User
from products.models import Product

class Order(BaseModel):
    ORDER_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    payment_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at']

    @property
    def subtotal(self):
        return self.price * self.quantity 