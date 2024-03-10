# models.py em sua aplicação Vendas

from django.db import models
from django.utils import timezone

class Sale(models.Model):
    sale_time = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Venda em {self.sale_time} - Total: {self.total_amount}"
