# views.py em sua aplicação Dashboard
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Vendas.models import Sale
from Order.models import Order
from Estoque.models import Product
from datetime import date, timedelta

class DashboardView(APIView):
    def get(self, request):
        total_products_in_stock = Product.objects.aggregate(Sum('quantidade_em_estoque'))['quantidade_em_estoque__sum'] or 0
        total_orders = Order.objects.count()
        last_month = date.today() - timedelta(days=30)
        sales_last_month = Sale.objects.filter(order__finished=True, sale_time__gte=last_month).count()

        data = {
            'total_products_in_stock': total_products_in_stock,
            'total_orders': total_orders,
            'sales_last_month': sales_last_month,
           
        }

        return Response(data, status=status.HTTP_200_OK)
