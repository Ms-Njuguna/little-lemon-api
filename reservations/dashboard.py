from datetime import date as date_cls
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Reservation, DiningTable, TimeSlot


@extend_schema(
    description="Staff dashboard stats (today, upcoming, completed, tables count, utilization). Staff/admin only."
)
class DashboardStatsView(APIView):
    def get(self, request):
        # Staff/admin only
        if not request.user.is_authenticated or request.user.role not in ["staff", "admin"]:
            return Response(
                {"detail": "Only staff/admin can access dashboard stats."},
                status=status.HTTP_403_FORBIDDEN,
            )

        today = date_cls.today()

        active_tables_count = DiningTable.objects.filter(is_active=True).count()

        today_qs = Reservation.objects.filter(date=today)

        today_total = today_qs.count()
        today_by_status = dict(
            today_qs.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        upcoming_count = Reservation.objects.filter(date__gt=today).count()
        completed_count = Reservation.objects.filter(status="completed").count()

        # Utilization: unique tables reserved today / active tables
        reserved_table_ids_today = today_qs.values_list("table_id", flat=True).distinct()
        reserved_tables_today_count = DiningTable.objects.filter(
            id__in=reserved_table_ids_today,
            is_active=True,
        ).count()

        utilization_pct = 0.0
        if active_tables_count > 0:
            utilization_pct = round((reserved_tables_today_count / active_tables_count) * 100, 2)

        # Utilization by time slot today
        utilization_by_slot_today = []

        time_slots_today = TimeSlot.objects.filter(is_active=True).order_by("start_time")

        for slot in time_slots_today:

            reserved_table_ids = Reservation.objects.filter(
                date=today,
                time_slot=slot
            ).values_list("table_id", flat=True).distinct()

            reserved_tables_count = DiningTable.objects.filter(
                id__in=reserved_table_ids,
                is_active=True
            ).count()

            slot_utilization_pct = 0.0
            if active_tables_count > 0:
                slot_utilization_pct = round(
                    (reserved_tables_count / active_tables_count) * 100, 2
                )

            utilization_by_slot_today.append({
                "time_slot_id": slot.id,
                "label": slot.label,
                "reserved_tables": reserved_tables_count,
                "active_tables": active_tables_count,
                "utilization_pct": slot_utilization_pct,
            })

        return Response(
            {
                "date": str(today),

                "tables": {
                    "active_tables": active_tables_count,
                    "reserved_tables_today": reserved_tables_today_count,
                    "utilization_pct_today": utilization_pct,
                },

                "reservations": {
                    "today_total": today_total,
                    "today_by_status": today_by_status,
                    "upcoming_total": upcoming_count,
                    "completed_total": completed_count,
                },

                "utilization_by_slot_today": utilization_by_slot_today,
            }
        )