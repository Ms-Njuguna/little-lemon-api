from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiningTableViewSet, TimeSlotViewSet, ReservationViewSet

router = DefaultRouter()
router.register("tables", DiningTableViewSet)
router.register("time-slots", TimeSlotViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]