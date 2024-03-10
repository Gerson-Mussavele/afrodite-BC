# api/models.py
from django.db import models
from Order.models import Order

class Sale(models.Model):
    sale_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales')
    def __str__(self):
        return f"Venda em {self.sale_time} - Total: {self.total_amount}"

class Order(models.Model):
    table_number = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.table_number}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)
    available_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Produto: {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
