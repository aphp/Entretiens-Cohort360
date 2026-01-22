"""
Medical Views - API endpoints for medical resources.

Pre-implemented:
- PatientViewSet: GET /Patient
- MedicationViewSet: GET /Medication

TODO (Exercise): Implement PrescriptionViewSet
See docs/exercises/django/README.md for specifications.
"""

from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Medication, Patient
from .serializers import MedicationSerializer, PatientSerializer


class StandardPagination(PageNumberPagination):
    """Standard pagination for all viewsets."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# =============================================================================
# Patient API
# =============================================================================


class PatientFilter(filters.FilterSet):
    """Filter for Patient queries."""

    # Support both French and English field names
    nom = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    prenom = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    date_naissance = filters.DateFilter(field_name="birth_date")
    birth_date = filters.DateFilter(field_name="birth_date")

    class Meta:
        model = Patient
        fields = ["status"]


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for patients.

    GET /Patient - List all patients
    GET /Patient/{id} - Get patient by ID

    Filters:
    - nom/last_name: Filter by last name (icontains)
    - prenom/first_name: Filter by first name (icontains)
    - date_naissance/birth_date: Filter by birth date
    - status: Filter by status (actif/suppr)
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = StandardPagination
    filterset_class = PatientFilter


# =============================================================================
# Medication API
# =============================================================================


class MedicationFilter(filters.FilterSet):
    """Filter for Medication queries."""

    code = filters.CharFilter(lookup_expr="icontains")
    label = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Medication
        fields = ["status"]


class MedicationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for medications.

    GET /Medication - List all medications
    GET /Medication/{id} - Get medication by ID

    Filters:
    - code: Filter by code (icontains)
    - label: Filter by label (icontains)
    - status: Filter by status (actif/suppr)
    """

    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    pagination_class = StandardPagination
    filterset_class = MedicationFilter


# =============================================================================
# TODO: Implement PrescriptionViewSet here
# =============================================================================
#
# Requirements:
# - GET /Prescription - List with filters
# - POST /Prescription - Create new prescription
# - PATCH /Prescription/{id} - Update prescription
#
# Filters:
# - patient: exact match
# - medication: exact match
# - status: exact match
# - start_date_from, start_date_to: date range
# - end_date_from, end_date_to: date range
#
# Example:
# class PrescriptionViewSet(viewsets.ModelViewSet):
#     queryset = Prescription.objects.all()
#     serializer_class = PrescriptionSerializer
#     pagination_class = StandardPagination
#     filterset_class = PrescriptionFilter
# =============================================================================
