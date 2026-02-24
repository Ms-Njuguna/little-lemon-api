from rest_framework import serializers
from .models import DiningTable, TimeSlot, Reservation

class DiningTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningTable
        fields = "__all__"

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "time_slot", "date", "guests", "status", "special_request", "created_at"]
        read_only_fields = ["id", "status", "created_at"]