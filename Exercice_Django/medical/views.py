from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Patient, Medication
from .filters import PatientFilter, MedicationFilter
from .serializers import PatientSerializer, MedicationSerializer
from .models import Prescription
from .serializers import PrescriptionSerializer
from .filters import PrescriptionFilter


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule des patients avec filtrage via query params."""

    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientFilter


class MedicationViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule des médicaments avec filtrage via query params."""

    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicationFilter


class PrescriptionViewSet(viewsets.ModelViewSet):
    """CRUD complet des prescriptions avec filtrage via query params."""

    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.select_related("patient", "medication").all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrescriptionFilter