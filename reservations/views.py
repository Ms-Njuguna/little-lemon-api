from rest_framework import viewsets, permissions
from .models import DiningTable, TimeSlot, Reservation
from .serializers import ReservationStatusSerializer, DiningTableSerializer, TimeSlotSerializer, ReservationSerializer, ReservationCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import permissions, status
from rest_framework import status as http_status
from datetime import date as date_cls
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .permissions import ReadOnlyOrStaff, IsOwnerOrStaff
from rest_framework.permissions import IsAuthenticated

from .services import get_available_tables

class DiningTableViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DiningTable.objects.all().order_by("table_number")
    serializer_class = DiningTableSerializer
    permission_classes = [ReadOnlyOrStaff]

class TimeSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = TimeSlot.objects.all().order_by("start_time")
    serializer_class = TimeSlotSerializer
    permission_classes = [ReadOnlyOrStaff]

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    queryset = Reservation.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return ReservationCreateSerializer
        return ReservationSerializer

    def get_queryset(self):
        user = self.request.user

        # Staff/admin see all
        if user.role in ["staff", "admin"]:
            return Reservation.objects.all()

        # Customers see only theirs
        return Reservation.objects.filter(user=user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        time_slot = serializer.validated_data["time_slot"]
        booking_date = serializer.validated_data["date"]
        guests = serializer.validated_data["guests"]

        # 1) slot must be active
        if not TimeSlot.objects.filter(id=time_slot.id, is_active=True).exists():
            return Response({"detail": "This time slot is not active."}, status=400)

        # 2) find available tables
        _, available = get_available_tables(date=booking_date, time_slot_id=time_slot.id, guests=guests)

        if not available:
            return Response({"detail": "No tables available for that date/time/guests."}, status=409)

        chosen_table = available[0]  # smallest fitting, due to ordering

        reservation = Reservation.objects.create(
            user=request.user,
            table=chosen_table,
            time_slot=time_slot,
            date=booking_date,
            guests=guests,
            special_request=serializer.validated_data.get("special_request", ""),
            status="pending",
        )

        output = ReservationSerializer(reservation).data
        return Response(output, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        if self.action in ["partial_update", "update"]:
            # Only allow status edits via PATCH/PUT
            return ReservationStatusSerializer
        return ReservationSerializer

    def partial_update(self, request, *args, **kwargs):
        reservation = self.get_object()  # IsOwnerOrStaff applies here

        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data.get("status")
        if new_status is None:
            return Response({"detail": "Provide 'status'."}, status=http_status.HTTP_400_BAD_REQUEST)

        user_role = request.user.role

        if user_role == "customer":
            if new_status != "cancelled":
                return Response(
                    {"detail": "Customers can only cancel reservations."},
                    status=http_status.HTTP_403_FORBIDDEN,
                )

        if user_role in ["staff", "admin"]:
            if new_status not in ["confirmed", "completed", "cancelled", "pending"]:
                return Response(
                    {"detail": "Invalid status value."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

        reservation.status = new_status
        reservation.save(update_fields=["status"])

        return Response(ReservationSerializer(reservation).data, status=http_status.HTTP_200_OK)

class AvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="date", required=True, type=str, description="YYYY-MM-DD"),
            OpenApiParameter(name="time_slot_id", required=True, type=int, description="TimeSlot id"),
            OpenApiParameter(name="guests", required=True, type=int, description="Number of guests"),
        ],
        examples=[
            OpenApiExample(
                "Example request",
                value={"date": "2026-03-01", "time_slot_id": 2, "guests": 4},
                request_only=True,
            ),
        ],
    )

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

        slot, tables = get_available_tables(
            date=booking_date,
            time_slot_id=time_slot_id,
            guests=guests
        )

        # If slot doesn't exist or inactive
        if slot is None:
           return Response(
                {"detail": "Time slot not found or inactive."},
                status=404
            )

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