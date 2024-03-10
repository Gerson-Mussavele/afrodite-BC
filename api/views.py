from rest_framework import generics, permissions
from .models import Sale, Order, Product
from .serializers import SaleSerializer, OrderSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import logging
from rest_framework.views import APIView
from datetime import date, timedelta
from django.db.models import Sum
from restaurante.permissions import IsAdminOrCashier, IsAdminOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import JsonResponse
logger = logging.getLogger(__name__)

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            logger.error(f"Error creating order. Validation errors: {serializer.errors}")
            return JsonResponse(serializer.errors, status=400)

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # @action(detail=True, methods=['put'])
    # def finish_order(self, request, *args, **kwargs):
    #     order = self.get_object()

    #     if order.finished:
    #         return Response({'message': 'Pedido já finalizado.'}, status=status.HTTP_400_BAD_REQUEST)

    #     order.finished = True
    #     order.save()
    #     logger.info(f'User: {request.user}, Method: {request.method}, Action: {self.action}')

    #     return Response({'message': 'Pedido finalizado com sucesso!'})

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrCashier])
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    

@authentication_classes([SessionAuthentication])
#@permission_classes([IsAdminOrReadOnly])
class DashboardView(APIView):
    def get(self, request):
        # Somente usuários com permissão de leitura podem acessar este endpoint
        total_products_in_stock = Product.objects.aggregate(Sum('available_quantity'))['available_quantity__sum'] or 0
        total_orders = Order.objects.count()
        last_month = date.today() - timedelta(days=30)
        sales_last_month = Sale.objects.filter(order__finish_order=True, sale_time__gte=last_month).count()

        data = {
            'total_products_in_stock': total_products_in_stock,
            'total_orders': total_orders,
            'sales_last_month': sales_last_month,
        }

        # Você precisa criar este serializer
        return Response(data, status=status.HTTP_200_OK)
