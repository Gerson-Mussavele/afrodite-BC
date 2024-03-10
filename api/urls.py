from django.urls import path
from .views import (
    SaleListCreateView,
    SaleDetailView,
    OrderListCreateView,
    OrderDetailView,
    ProductListCreateView,
    ProductDetailView,
    DashboardView,
)

from Order.views import(
    OrderFinishView
)

urlpatterns = [
    path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('sales/<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),


    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    #path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-finish'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]