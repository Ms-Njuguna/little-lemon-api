from rest_framework import viewsets, permissions
from .models import DiningTable, TimeSlot, Reservation
from .serializers import DiningTableSerializer, TimeSlotSerializer, ReservationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from datetime import date as date_cls

from .services import get_available_tables

class DiningTableViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DiningTable.objects.all().order_by("table_number")
    serializer_class = DiningTableSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = TimeSlot.objects.all().order_by("start_time")
    serializer_class = TimeSlotSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reservation.objects.all().order_by("-created_at")
    serializer_class = ReservationSerializer

class AvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_str = request.query_params.get("date")
        time_slot_id = request.query_params.get("time_slot_id")
        guests = request.query_params.get("guests")

        if not date_str or not time_slot_id or not guests:
            return Response(
                {"detail": "Required query params: date, time_slot_id, guests"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            booking_date = date_cls.fromisoformat(date_str)
            time_slot_id = int(time_slot_id)
            guests = int(guests)
        except ValueError:
            return Response({"detail": "Invalid date/time_slot_id/guests format."}, status=400)

        slot, tables = get_available_tables(date=booking_date, time_slot_id=time_slot_id, guests=guests)

        if slot == []:
            # This won't happen due to our logic, but leaving it safe
            pass

        if slot is None:
            return Response({"detail": "Time slot not found."}, status=404)

        # if slot exists but inactive, we returned empty list via DoesNotExist logic
        if isinstance(slot, list):
            return Response({"detail": "Time slot not active."}, status=400)

        return Response({
            "date": date_str,
            "time_slot": {"id": slot.id, "label": slot.label, "start_time": str(slot.start_time), "end_time": str(slot.end_time)},
            "guests": guests,
            "available_tables": [
                {"id": t.id, "table_number": t.table_number, "capacity": t.capacity, "location": t.location}
                for t in tables
            ],
        })