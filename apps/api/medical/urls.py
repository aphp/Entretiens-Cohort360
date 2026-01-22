"""
Medical URL Configuration.

Pre-configured routes:
- /Patient - Patient API
- /Medication - Medication API

TODO (Exercise): Add /Prescription route
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MedicationViewSet, PatientViewSet

router = DefaultRouter()
router.register(r"Patient", PatientViewSet, basename="patient")
router.register(r"Medication", MedicationViewSet, basename="medication")

# =============================================================================
# TODO: Register PrescriptionViewSet
# =============================================================================
# router.register(r"Prescription", PrescriptionViewSet, basename="prescription")
# =============================================================================

urlpatterns = [
    path("", include(router.urls)),
]
