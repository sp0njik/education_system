from rest_framework import permissions


class ProductAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, product):
        return request.user.has_access(product)
