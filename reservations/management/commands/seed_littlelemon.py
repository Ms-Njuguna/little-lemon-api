from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reservations.models import DiningTable, TimeSlot
from datetime import time

User = get_user_model()

class Command(BaseCommand):
    help = "Seed Little Lemon with demo tables, timeslots, and a staff user."

    def handle(self, *args, **options):
        # 1) Staff user
        staff_email = "staff@littlelemon.com"
        staff_password = "password1234"

        staff, created = User.objects.get_or_create(
            email=staff_email,
            defaults={
                "full_name": "Little Lemon Staff",
                "phone": "0700000000",
                "role": "staff",
                "is_active": True,
                "is_staff": True,
                "is_email_verified": True,
            },
        )
        if created:
            staff.set_password(staff_password)
            staff.save()
            self.stdout.write(self.style.SUCCESS(f"✅ Created staff user: {staff_email} / {staff_password}"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Staff user already exists: {staff_email}"))

        # 2) Tables (10)
        tables = [
            (1, 2, "Inside"),
            (2, 2, "Inside"),
            (3, 4, "Window"),
            (4, 4, "Window"),
            (5, 4, "Inside"),
            (6, 6, "Patio"),
            (7, 6, "Patio"),
            (8, 8, "Patio"),
            (9, 2, "Bar"),
            (10, 4, "Bar"),
        ]

        created_count = 0
        for number, cap, location in tables:
            _, created = DiningTable.objects.get_or_create(
                table_number=number,
                defaults={"capacity": cap, "location": location, "is_active": True},
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Tables seeded (new): {created_count}"))

        # 3) Time slots (6)
        slots = [
            ("Breakfast", time(8, 0), time(10, 0)),
            ("Brunch", time(10, 0), time(12, 0)),
            ("Lunch", time(12, 0), time(14, 0)),
            ("Afternoon", time(14, 0), time(17, 0)),
            ("Dinner", time(18, 0), time(21, 0)),
            ("Late Dinner", time(21, 0), time(23, 0)),
        ]

        created_slots = 0
        for label, start, end in slots:
            _, created = TimeSlot.objects.get_or_create(
                label=label,
                defaults={"start_time": start, "end_time": end, "is_active": True},
            )
            if created:
                created_slots += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Time slots seeded (new): {created_slots}"))

        self.stdout.write(self.style.SUCCESS("🎉 Seeding complete."))