from django.urls import path
from .views import PatientListView, MedicationListView


urlpatterns = [
    path("Patient", PatientListView.as_view(), name="patient-list"),
    path("Medication", MedicationListView.as_view(), name="medication-list"),
]
