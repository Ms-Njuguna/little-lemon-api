from datetime import date as date_cls
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
        fields = ["id", "time_slot", "date", "guests", "special_request"]
        read_only_fields = ["id"]

    def validate_date(self, value):
        if value < date_cls.today():
            raise serializers.ValidationError("You can't book a reservation in the past.")
        return value

    def validate_guests(self, value):
        if value < 1:
            raise serializers.ValidationError("Guests must be at least 1.")
        if value > 12:
            raise serializers.ValidationError("Guests cannot exceed 12 for online booking.")
        return value

    def validate_time_slot(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This time slot is not active.")
        return value

class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["status"]