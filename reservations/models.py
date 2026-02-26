from django.db import models
from django.conf import settings

class DiningTable(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} ({self.capacity})"

class TimeSlot(models.Model):
    label = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label} ({self.start_time}-{self.end_time})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(DiningTable, on_delete=models.PROTECT, related_name="reservations")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name="reservations")

    date = models.DateField()
    guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["table", "date", "time_slot"], name="uniq_table_date_slot")
        ]

    def __str__(self):
        return f"{self.user.email} - Table {self.table.table_number} on {self.date} ({self.time_slot.label})"