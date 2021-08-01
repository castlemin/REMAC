from .views import CustomUserViewSet, RequestViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', CustomUserViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'product', ProductViewSet)

urlpatterns = router.urls
