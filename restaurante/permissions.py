
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        # Permite leitura para todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permite gravação apenas para administradores
        return request.user and request.user.groups.filter(name='Administrador').exists()

class IsCashier(permissions.BasePermission):
    """
    Custom permission to only allow cashiers to access order-related actions.
    """
    def has_permission(self, request, view):
        # Permite apenas para caixas
        return request.user and request.user.groups.filter(name='caixa').exists()

class IsAdminOrCashier(permissions.BasePermission):
    """
    Custom permission to allow admins to do everything and cashiers only order-related actions.
    """
    def has_permission(self, request, view):
        # Permite leitura para todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permite gravação apenas para administradores e para ações relacionadas a pedidos para caixas
        return (
            (request.user and request.user.groups.filter(name='Administrador').exists()) or
            (request.user and request.user.groups.filter(name='caixa').exists() and view.action in ['create', 'update', 'partial_update', 'destroy', 'finish_order'])
        )
