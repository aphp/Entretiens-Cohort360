from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, exceptions
from django.core.exceptions import ValidationError

from .models import Patient, Medication, Prescription
from .filters import PatientFilter, MedicationFilter, PrescriptionFilter
from .serializers import PatientSerializer, MedicationSerializer, PrescriptionSerializer


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


class PrescriptionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    #    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Creation et lecture des prescriptions avec filtrage via query params."""

    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrescriptionFilter

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise exceptions.ValidationError(e.message)
