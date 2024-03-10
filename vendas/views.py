from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Order.models import Order

@method_decorator(csrf_exempt, name='dispatch')
class SaleListView(View):
    def get_queryset(self):
        # Ajuste a consulta para refletir a estrutura real do seu modelo
        return Order.objects.filter(order__finished=True)

    def get(self, request):
        try:
            # Filtrar apenas as vendas relacionadas aos pedidos finalizados
            orders = self.get_queryset()

            # Estruturar os dados para a resposta JSON
            orders_data = [{'id': Order.id, 'order_time': Order.Order_time, 'total_amount': float(Order.total_amount)} for order in orders]

            return JsonResponse({'orders': orders_data})
        except Exception as e:
            return JsonResponse({'error': f'Erro ao buscar vendas: {str(e)}'}, status=500)