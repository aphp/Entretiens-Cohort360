from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .models import Patient, Medication, MedicationRequest
from .filters import PatientFilter, MedicationFilter, MedicationRequestFilter
from .serializers import PatientSerializer, MedicationSerializer, MedicationRequestSerializer


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


class MedicationRequestViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    """FHIR R4 MedicationRequest — lecture, création et mise à jour."""

    serializer_class = MedicationRequestSerializer
    queryset = MedicationRequest.objects.select_related("subject", "medication_reference").all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicationRequestFilter
