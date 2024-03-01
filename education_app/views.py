from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from education_app.models import Product
from education_app.serializers import ProductSerializer, ProductLessonsSerializer

from education_app.permissions import ProductAccessPermission


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('author').prefetch_related('lessons').all()

    def get_serializer_class(self):
        if self.action == 'retrive':
            return ProductLessonsSerializer
        return ProductSerializer

    @permission_classes([IsAuthenticated, ProductAccessPermission])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
