from typing import Any

from django.db.models import QuerySet
from rest_framework.generics import ListAPIView

from .models import Patient, Medication
from .serializers import PatientSerializer, MedicationSerializer


class PatientListView(ListAPIView):
    """Endpoint en lecture seule pour lister les patients avec filtrage simple."""

    serializer_class = PatientSerializer

    def get_queryset(self) -> QuerySet[Patient]:
        qs = Patient.objects.all()
        params = self.request.query_params

        # Alias FR → champs
        nom = params.get("nom") or params.get("last_name")
        prenom = params.get("prenom") or params.get("first_name")
        date_naissance = params.get("date_naissance") or params.get("birth_date")

        if nom:
            qs = qs.filter(last_name__icontains=nom)
        if prenom:
            qs = qs.filter(first_name__icontains=prenom)
        if date_naissance:
            qs = qs.filter(birth_date=date_naissance)

        return qs


class MedicationListView(ListAPIView):
    """Endpoint en lecture seule pour lister les médicaments avec filtrage simple."""

    serializer_class = MedicationSerializer

    def get_queryset(self) -> QuerySet[Medication]:
        qs = Medication.objects.all()
        params = self.request.query_params

        code = params.get("code")
        label = params.get("label")
        status = params.get("status")

        if code:
            qs = qs.filter(code__icontains=code)
        if label:
            qs = qs.filter(label__icontains=label)
        if status:
            qs = qs.filter(status=status.lower())

        return qs
