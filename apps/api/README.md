# Django REST API - Prescription Management

API backend for the Cohort360 prescription management exercise.

## Quick Start

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo --patients 100 --medications 30
uv run python manage.py runserver
```

## Endpoints

- `GET /Patient` - List patients
- `GET /Medication` - List medications
- `GET /Prescription` - List prescriptions (TODO)
- `POST /Prescription` - Create prescription (TODO)
- `PATCH /Prescription/:id` - Update prescription (TODO)

See [docs/exercises/django/README.md](../../docs/exercises/django/README.md) for exercise specifications.
