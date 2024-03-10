# models.py em sua aplicação Order

from django.db import models
from Estoque.models import Product  # Importe o modelo Product

class Order(models.Model):
    table = models.IntegerField() 
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)  

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.table}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
       
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)