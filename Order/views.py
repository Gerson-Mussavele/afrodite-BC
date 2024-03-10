import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from vendas.models import Sale as VendaSale
from .models import OrderItem, Order
from Estoque.models import Product
from django.views.decorators.http import require_POST
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

#@method_decorator(csrf_exempt, name='dispatch')
class OrderUpdateView(View):
    @csrf_exempt
    def put(self, request, pk):
        try:
            print(f'Recebida requisição PUT para /api/orders/{pk}')

            order = get_object_or_404(Order, pk=pk)
            data = json.loads(request.body)

            table = data.get('table', order.table)
            finish_order = data.get('finish_order', False)
            payment_method = data.get('payment_method', '')

            order.table = table
            order.save()

            for item_data in data.get('items', []):
                product_name = item_data.get('product')
                quantity = item_data.get('quantity', 0)
                subtotal = item_data.get('subtotal', 0.0)

                product = get_object_or_404(Product, name=product_name)
                order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

                if not created:
                    order_item.quantity = quantity
                    order_item.subtotal = subtotal
                    order_item.save()

            updated_total_amount = OrderItem.objects.filter(order=order).aggregate(total=Sum('subtotal'))['total'] or 0
            order.total_amount = updated_total_amount
            order.save()

            return JsonResponse({'message': 'Pedido atualizado com sucesso!'})
        except (ValueError, KeyError) as e:
            return JsonResponse({'error': f'Dados inválidos: {e}'}, status=400)
        except Exception as e:
            logger.error(f'Erro na view OrderUpdateView: {e}', exc_info=True)
            return JsonResponse({'error': f'Erro ao processar a atualização do pedido: {e}'}, status=500)

class OrderFinishView(View):
    @csrf_exempt
    def patch(self, request, pk):
        try:
            # logger.info()
            print('Método finish_order chamado! ', pk)
            order = Order.objects.filter(pk=pk).exists()
            # orders =Order.objects.all()

            # if order.finished:
            #     return JsonResponse({'message': 'Pedido já finalizado.'}, status=status.HTTP_400_BAD_REQUEST)

            # order.finished = True
            # order.save()
            # logger.info(f'User: {request.user}, Method: {request.method}')

            # venda_sale = VendaSale.objects.create(order=order, total_amount=order.total_amount)

            return JsonResponse({'message': 'Pedido finalizado com sucesso!', "pk": order})
        except Exception as e:
            logger.error(f'Erro na view OrderFinishView: {e}', exc_info=True)

            return JsonResponse({'error': f'Erro ao finalizar o pedido: {e}'}, status=404)


class CreateOrderView(View):
    @csrf_exempt  
    @require_POST
    #@login_required
    def post(self, request):
        print("Heyyy")
        try:
            data = json.loads(request.body)
            print("Received data:", data)

            table = data.get('table', '')
            items = data.get('items', [])

            if not table or not items:
                raise ValueError("Dados inválidos. Certifique-se de fornecer uma mesa e itens.")

            with transaction.atomic():
                
                order = Order.objects.create(table=table)
                total_amount = 0

                for item_data in items:
                    product_id = item_data.get('product_id', '')
                    quantity = int(item_data.get('quantity', 1))

                    if not product_id or quantity <= 0:
                        raise ValueError("Dados do item inválidos.")

                    product = get_object_or_404(Product, pk=product_id)

                    if product.quantidade_em_estoque < quantity:
                        raise ValueError(f"Quantidade insuficiente em estoque para o produto: {product.name}")

                    subtotal = product.price * quantity

                    OrderItem.objects.create(order=order, product=product, quantity=quantity, subtotal=subtotal)
                    total_amount += subtotal

                    product.quantidade_em_estoque -= quantity
                    product.save()

                order.total_amount = total_amount
                order.save()

            return JsonResponse({'message': 'Pedido criado com sucesso.', 'order_id': order.id})
        except (ValueError, KeyError) as e:
            print(f'Erro de validação: {e}')
            return JsonResponse({'error': f'Dados inválidos: {e}'}, status=400)
        except Exception as e:
            print(f'Erro na view CreateOrderView: {e}')
            logger.error(f'Erro na view CreateOrderView: {e}', exc_info=True)
            return JsonResponse({'error': f'Erro ao processar a criação do pedido: {e}'}, status=500)


class OrderListView(View):
    # @login_required
    def get(self, request):
        try:
            orders = Order.objects.all()

            
            orders_data = orders.values(
                'id',
                'table',
                'total_amount'
            ).prefetch_related(
                'items__product'
            )

            return JsonResponse({'orders': list(orders_data)})
        except Exception as e:
           
            logger.error(f'Erro ao recuperar pedidos: {e}', exc_info=True)
            return JsonResponse({'error': 'Erro ao recuperar pedidos'}, status=500)
