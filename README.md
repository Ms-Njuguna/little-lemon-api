# Little Lemon API (Django + DRF)

A production-style restaurant reservations backend powering the Little Lemon frontend.

---

## Features

- JWT Auth (login/signup/refresh)
- Role-based permissions (customer vs staff/admin)
- Tables + Time Slots management
- Availability search (date + slot + guests)
- Reservation lifecycle:
    - Create (auto-assign best table)
    - Upcoming reservations
    - Cancel / Confirm / Complete
- Staff dashboard stats + utilization by time slot
- Swagger UI + ReDoc docs
- PostgreSQL database

---

## Tech Stack

- Django, Django REST Framework
- PostgreSQL
- drf-spectacular (OpenAPI/Swagger)
- Gunicorn + Nginx (prod)

---

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_littlelemon
python manage.py runserver
```

---

## Environment Variables

- Create .env:
```bash
DJANGO_SECRET_KEY
DJANGO_DEBUG
ALLOWED_HOSTS
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
CORS_ALLOWED_ORIGINS
```

---

## API Docs

- Swagger: /api/docs/
- ReDoc: /api/redoc/

### Core Endpoints

- **Auth**
    - POST /api/auth/signup/
    - POST /api/auth/login/
    - POST /api/auth/refresh/
    - GET /api/me/

- **Reservations**
    - GET/POST /api/reservations/
    - GET /api/reservations/upcoming/
    - POST /api/reservations/{id}/cancel/
    - POST /api/reservations/{id}/confirm/ (staff/admin)
    - POST /api/reservations/{id}/complete/ (staff/admin)

- **Availability**
    - GET /api/availability/?date=YYYY-MM-DD&time_slot_id=1&guests=4

- **Dashboard (staff/admin)**
    - GET /api/dashboard/stats/

---