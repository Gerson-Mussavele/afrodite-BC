from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)
    quantidade_em_estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Produto: {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Crie uma instância de Estoque sem depender diretamente do modelo Estoque
        Product.objects.create(
            name=self.name,
            price=self.price,
            category=self.category,
            quantidade_em_estoque=self.quantidade_em_estoque
        )

# Importe Estoque aqui fora para evitar ciclos de importação

