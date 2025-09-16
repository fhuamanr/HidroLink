from rest_framework.routers import DefaultRouter
from .views import HouseholdViewSet, DeviceViewSet, ReadingViewSet, AlertViewSet, GoalViewSet

router = DefaultRouter()
router.register(r"households", HouseholdViewSet)
router.register(r"devices", DeviceViewSet)
router.register(r"readings", ReadingViewSet)
router.register(r"alerts", AlertViewSet)
router.register(r"goals", GoalViewSet)

urlpatterns = router.urls