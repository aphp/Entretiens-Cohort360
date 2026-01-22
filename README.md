# 🏥 Cohort360 Fullstack Exercise - Starter

> **Turborepo monorepo starter for the AP-HP technical interview**

This is the **starter template** for building the Prescription Management API and UI.
The Patient and Medication models are pre-implemented; your task is to add the Prescription feature.

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 22+ and npm
- **Python** 3.12+ with [uv](https://docs.astral.sh/uv/)
- **Git**

### Setup

```bash
# Clone and install
git clone https://github.com/aphp/Entretiens-Cohort360.git
cd Entretiens-Cohort360
git checkout boilerplate/starter
npm install

# Setup Django
cd apps/api
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo --patients 100 --medications 30
cd ../..

# Start development
npm run dev
```

### Access

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/admin/

---

## 📋 Exercise Overview

| Exercise | Estimated Time | Documentation |
|----------|----------------|---------------|
| **Backend (Django)** | ~1h | [docs/exercises/django/README.md](docs/exercises/django/README.md) |
| **Frontend (React)** | ~1h30-2h | [docs/exercises/react/README.md](docs/exercises/react/README.md) |

### What's Pre-Implemented ✅

- Patient model and API (`GET /Patient`)
- Medication model and API (`GET /Medication`)
- Django REST Framework setup with pagination
- React app with TanStack Query
- Axios API client
- TypeScript types
- Test scaffolds
- E2E test patterns

### What You Need to Build 🔨

1. **Django Prescription Model**
   - ForeignKey to Patient and Medication
   - Date range (start_date, end_date)
   - Status enum (valide, en_attente, suppr)

2. **Django Prescription API**
   - `GET /Prescription` with filters
   - `POST /Prescription`
   - `PATCH /Prescription/:id`

3. **React Prescription UI**
   - List with pagination
   - Create/Edit forms
   - Filters
   - Soft delete

---

## 🏗️ Project Structure

```
├── apps/
│   ├── api/                 # Django REST API
│   │   ├── config/          # Django settings
│   │   └── medical/         # Medical app
│   │       ├── models.py    # Patient, Medication (+ TODO: Prescription)
│   │       ├── views.py     # ViewSets (+ TODO: PrescriptionViewSet)
│   │       └── tests/       # API tests
│   └── web/                 # React frontend
│       └── src/
│           ├── App.tsx      # Main component (TODO: build UI)
│           ├── api/         # API client
│           └── types/       # TypeScript interfaces
├── docs/exercises/          # Exercise specifications
├── e2e/                     # Playwright E2E tests
├── packages/                # Shared configs
├── docker-compose.yml       # Docker development
└── .github/workflows/       # CI pipeline
```

---

## 🧪 Testing

```bash
# Django unit tests
cd apps/api && uv run python manage.py test

# React unit tests
cd apps/web && npm test

# E2E tests
npm run test:e2e
```

---

## 🐳 Docker (Optional)

```bash
docker compose up -d
```

---

## 📖 Resources

- [Django REST Framework](https://www.django-rest-framework.org/)
- [TanStack Query](https://tanstack.com/query)
- [React Hook Form](https://react-hook-form.com/)
- [Playwright](https://playwright.dev/)

---

## ✅ Acceptance Criteria

### Backend (MVP ~1h)

- [ ] Prescription model with all required fields
- [ ] GET /Prescription with pagination
- [ ] POST /Prescription with validation
- [ ] PATCH /Prescription/:id
- [ ] Filters: patient, medication, status, date ranges
- [ ] Unit tests passing

### Frontend

#### MVP (~2h)
- [ ] Prescription list with table
- [ ] Create prescription form
- [ ] Loading and error states

#### Stretch Goals (+1h)
- [ ] Edit prescription form
- [ ] Filter controls (patient, medication, status, dates)
- [ ] Soft delete (status → 'suppr')
- [ ] Unit tests passing

---

## 📦 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Django 5.2 + DRF | REST API |
| Frontend | React 19 + TypeScript | UI |
| Forms | React Hook Form + Zod | Validation |
| State | TanStack Query | Server state |
| Testing | Vitest + Playwright | Unit + E2E |
| DevOps | Docker + GitHub Actions | CI/CD |

---

**Good luck! 🎓**

