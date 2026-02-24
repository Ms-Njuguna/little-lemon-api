from .models import DiningTable, Reservation, TimeSlot


def get_available_tables(*, date, time_slot_id, guests):
    # Validate time slot exists and is active
    try:
        slot = TimeSlot.objects.get(id=time_slot_id, is_active=True)
    except TimeSlot.DoesNotExist:
        return None, []   # ✅ return None, not slot

    # Get reserved tables for that date and slot
    reserved_table_ids = Reservation.objects.filter(
        date=date,
        time_slot_id=time_slot_id,
    ).values_list("table_id", flat=True)

    # Get available tables
    tables = DiningTable.objects.filter(
        is_active=True,
        capacity__gte=guests,
    ).exclude(
        id__in=reserved_table_ids
    ).order_by("capacity", "table_number")

    return slot, list(tables)