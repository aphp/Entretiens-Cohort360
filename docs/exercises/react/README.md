# 🌐 React Frontend Exercise

> Prescription Management Web Application

## Exercise Specification

Build a React application to manage medical prescriptions with the following features:

### Required Features

1. **List Prescriptions**
   - Display all prescriptions in a table/list
   - Show patient name, medication, dates, status
   - Pagination support

2. **Create Prescription**
   - Form to create new prescriptions
   - Patient and medication selection
   - Date range picker (start/end dates)
   - Status selection
   - Optional comment field

3. **Edit Prescription**
   - Inline editing or modal form
   - Update any prescription field
   - Validation (end date > start date)

4. **Filter Prescriptions**
   - Filter by patient
   - Filter by medication
   - Filter by status
   - Filter by date range

5. **Delete Prescription**
   - Soft delete (change status to 'suppr')

---

## Implementation

### Tech Stack

| Technology | Purpose |
|------------|---------|
| React 19 | UI Framework |
| TypeScript 5.9 | Type safety |
| Vite | Build tool |
| TailwindCSS 4 | Styling (utility-first CSS) |
| TanStack Query | Server state management |
| TanStack Table | Data table with sorting/pagination |
| React Hook Form | Form handling |
| Zod | Schema validation |
| Axios | HTTP client |
| Vitest | Unit testing |

### Pre-built Components

The following components are **already provided** to save you time:

- `DataTable` - Sortable table with pagination (`src/components/DataTable.tsx`)
- `StatusBadge` - Status indicator component
- CSS utilities: `.btn`, `.btn-primary`, `.input`, `.card`, `.status-badge`

### Scaffold Files (with TODOs)

The following files are **scaffolded** with example code and TODO comments:

| File | Purpose |
|------|---------|
| `src/api/prescriptions.ts` | API CRUD functions (implement 4 functions) |
| `src/hooks/usePrescriptions.ts` | React Query hooks (mostly complete) |
| `src/components/PrescriptionList.tsx` | Table view (implement with DataTable) |
| `src/components/PrescriptionForm.tsx` | Create/edit form (implement with react-hook-form) |
| `src/components/PrescriptionFilters.tsx` | Filter panel (implement dropdowns + dates) |

**💡 Start with the API functions, then the hooks, then the components.**

### Project Structure

```
apps/web/
├── src/
│   ├── api/
│   │   ├── client.ts          # Axios instance
│   │   └── prescriptions.ts   # API functions
│   ├── components/
│   │   ├── PrescriptionForm.tsx
│   │   ├── PrescriptionList.tsx
│   │   └── PrescriptionFilters.tsx
│   ├── hooks/
│   │   └── usePrescriptions.ts # React Query hooks
│   ├── types/
│   │   └── index.ts           # TypeScript interfaces
│   ├── test/
│   │   ├── api.test.ts
│   │   └── components.test.tsx
│   ├── App.tsx
│   └── main.tsx
├── package.json
└── vite.config.ts
```

### Running the App

```bash
# From monorepo root
cd apps/web
npm install
npm run dev
```

### Testing

```bash
npm test              # Run tests once
npm run test:watch    # Watch mode
npm run test:coverage # With coverage
```

---

## API Integration

The frontend connects to the Django API at `http://127.0.0.1:8000`.

### Endpoints Used

- `GET /Patient` - List patients
- `GET /Medication` - List medications
- `GET /Prescription` - List prescriptions (with filters)
- `POST /Prescription` - Create prescription
- `PATCH /Prescription/:id` - Update prescription
- `DELETE /Prescription/:id` - Delete prescription

---

## Tests

### Pre-implemented (4 scaffold tests)
- API client configuration (2 tests)
- App component rendering (2 tests)

### TODO: Add Prescription tests
- API CRUD operations
- PrescriptionForm validation
- PrescriptionList rendering
- PrescriptionFilters behavior
