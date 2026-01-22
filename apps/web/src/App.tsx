/**
 * Cohort360 Prescriptions - Technical Interview Exercise
 *
 * Build a prescription management interface.
 *
 * Requirements:
 * 1. List prescriptions with pagination
 * 2. Create new prescriptions
 * 3. Edit existing prescriptions
 * 4. Filter by patient, medication, status, dates
 * 5. Soft delete (change status to 'suppr')
 *
 * You are free to choose your own approach for:
 * - State management (useState, useReducer, Zustand, etc.)
 * - Data fetching (fetch, axios, React Query, SWR, etc.)
 * - Form handling (controlled inputs, react-hook-form, etc.)
 * - UI components (build your own or use a library)
 *
 * API endpoints are available at http://localhost:8000/api/
 * See docs/exercises/react/README.md for API documentation.
 */

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            🏥 Cohort360 - Prescription Management
          </h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* TODO: Build your prescription management UI here */}
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500">Start building your solution here.</p>
        </div>
      </main>
    </div>
  );
}

export default App;
