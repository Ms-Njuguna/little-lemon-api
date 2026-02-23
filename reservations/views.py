from rest_framework import viewsets
from .models import DiningTable, TimeSlot, Reservation
from .serializers import DiningTableSerializer, TimeSlotSerializer, ReservationSerializer

class DiningTableViewSet(viewsets.ModelViewSet):
    queryset = DiningTable.objects.all().order_by("table_number")
    serializer_class = DiningTableSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all().order_by("start_time")
    serializer_class = TimeSlotSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer