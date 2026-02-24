from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiningTableViewSet, TimeSlotViewSet, ReservationViewSet, AvailabilityView
from .dashboard import DashboardStatsView

router = DefaultRouter()
router.register("tables", DiningTableViewSet)
router.register("time-slots", TimeSlotViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("availability/", AvailabilityView.as_view(), name="availability"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("", include(router.urls)),
]