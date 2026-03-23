from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Patient, Medication, Prescription
from .filters import PatientFilter, MedicationFilter
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


class PrescriptionViewSet(viewsets.ViewSet):
    """Prescription read-only with query params filtering."""

    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = MedicationFilter

    def list(self, request):
        queryset = Prescription.objects.all()
        serializer = PrescriptionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Prescription.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PrescriptionSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        pass
