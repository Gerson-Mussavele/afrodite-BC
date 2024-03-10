from django.contrib import admin
from django.urls import include, path


from Estoque.views import ProductListView, ProductDetailView, CreateProductView, UpdateProductView, DeleteProductView
from Order.views import CreateOrderView, OrderListView, OrderFinishView,OrderUpdateView
from api.views import DashboardView, OrderDetailView
from vendas.views import SaleListView



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('users.urls')),
    
    path('api/', include('api.urls')),

    

    # path('orders/', OrderListView.as_view(), name='order-list'),
    # path('orders/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    # path('createOrders/', CreateOrderView.as_view, name='create-order'),
    # path('orders/<int:pk>/', OrderFinishView.as_view(), name='order-finish'),




    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', CreateProductView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', UpdateProductView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', DeleteProductView.as_view(), name='product-delete'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('sales/', SaleListView.as_view(), name='sale-list'),

    path('api-auth/', include('rest_framework.urls')),

    
]
