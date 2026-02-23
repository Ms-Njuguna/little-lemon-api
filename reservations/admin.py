from django.contrib import admin
from .models import DiningTable, TimeSlot, Reservation

admin.site.register(DiningTable)
admin.site.register(TimeSlot)
admin.site.register(Reservation)