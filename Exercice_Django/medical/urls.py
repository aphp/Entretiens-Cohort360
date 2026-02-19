from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PatientViewSet, MedicationViewSet, MedicationRequestViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r"Patient", PatientViewSet, basename="patient")
router.register(r"Medication", MedicationViewSet, basename="medication")
router.register(r"MedicationRequest", MedicationRequestViewSet, basename="medicationrequest")

urlpatterns = [
    path("", include(router.urls)),
]
