from django.db import models
from common.models import BaseModel
from users.models import User
from products.models import Product

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    
    class Meta:
        ordering = ['-created_at']

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('cart', 'product') 