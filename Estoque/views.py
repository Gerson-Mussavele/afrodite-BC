from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import json
from .models import Product
from django.views.decorators.csrf import csrf_exempt
class ProductListView(View):
    @csrf_exempt
    def get(self, request):
        products = Product.objects.all()
        products_data = [{'id': product.id, 'name': product.name, 'price': float(product.price), 'category': product.category, 'quantity_em_estoque': product.quantidade_em_estoque} for product in products]
        print('Products Data:', products_data)
        return JsonResponse({'products': products_data})

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_data = {'id': product.id, 'name': product.name, 'price': float(product.price), 'category': product.category, 'quantity_em_estoque': product.quantidade_em_estoque}
        return JsonResponse({'product': product_data})

class CreateProductView(View):
    @csrf_exempt
    #@user_passes_test(lambda user: user.is_staff)
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            price = data.get('price', '')
            category = data.get('category', '')
            quantidade_em_estoque = data.get('quantidade_em_estoque', 0)

            if not (name and price and category):
                raise ValueError("Dados inválidos. Certifique-se de fornecer nome, preço e categoria.")

            product = Product.objects.create(
                name=name,
                price=price,
                category=category,
                quantidade_em_estoque=quantidade_em_estoque
            )

            product_data = {'id': product.id, 'name': product.name, 'price': float(product.price), 'category': product.category, 'quantity_em_estoque': product.quantidade_em_estoque}
            return JsonResponse({'message': 'Produto criado com sucesso.', 'product': product_data})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

class UpdateProductView(View):
    @csrf_exempt
    #@user_passes_test(lambda user: user.is_staff)
    def post(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk)

            data = json.loads(request.body)
            name = data.get('name', '')
            price = data.get('price', '')
            category = data.get('category', '')
            quantidade_em_estoque = data.get('quantidade_em_estoque', 0)

            if not (name and price and category):
                raise ValueError("Dados inválidos. Certifique-se de fornecer nome, preço e categoria.")

            product.name = name
            product.price = price
            product.category = category
            product.quantidade_em_estoque = quantidade_em_estoque
            product.save()

            product_data = {'id': product.id, 'name': product.name, 'price': float(product.price), 'category': product.category, 'quantity_em_estoque': product.quantidade_em_estoque}
            return JsonResponse({'message': 'Produto atualizado com sucesso.', 'product': product_data})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

class DeleteProductView(View):
    #@user_passes_test(lambda user: user.is_staff)
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return JsonResponse({'message': 'Produto excluído com sucesso.'})
