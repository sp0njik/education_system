from rest_framework.routers import DefaultRouter

from education_app.views import ProductViewSet

router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')

urlpatterns = router.urls
