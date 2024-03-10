# api/serializers.py
from rest_framework import serializers
from .models import Sale, Order, Product, OrderItem
import logging
from django.db import transaction
from decimal import Decimal
logger = logging.getLogger(__name__)

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

    # Crie o objeto Order sem usar o método 'create' do manager
        order = Order.objects.create(**validated_data)

        total_amount = Decimal('0.00')  # Inicialize o total_amount com zero

        for item_data in items_data:
            product = item_data['product']
            quantity = int(item_data['quantity'])
            price = Decimal(str(product.price))
            subtotal = price * quantity  # Calcule o subtotal do item
            total_amount += subtotal # Adicione o subtotal ao total_amount

        # Atualize o estoque do produto
            if product.available_quantity < quantity:
                raise serializers.ValidationError(f"Quantidade insuficiente em estoque para o produto: {product.name}")

            product.available_quantity -= quantity
            product.save()

        # Utilize o objeto Product diretamente
            OrderItem.objects.create(order=order, product=product, quantity=quantity, subtotal=subtotal)

        order.total_amount = total_amount  # Atribua o total_amount ao campo total_amount do pedido
        order.save()  # Salve o pedido com o total_amount calculado

        return order


    def update(self, instance, validated_data):
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.finished = validated_data.get('finished', instance.finished)
        instance.save()

        items_data = validated_data.get('items', [])
        existing_items_by_id = {item.id: item for item in instance.items.all()}

        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id and item_id in existing_items_by_id:
                item_instance = existing_items_by_id[item_id]
                item_instance.product = item_data.get('product', item_instance.product)
                item_instance.quantity = item_data.get('quantity', item_instance.quantity)
                item_instance.save()
            else:
                OrderItem.objects.create(
                    order=instance,
                    product=item_data.get('product'),
                    quantity=item_data.get('quantity'),
                    subtotal=item_data.get('subtotal')
                )

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items'] = OrderItemSerializer(instance.items.all(), many=True).data
        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
