"""
Medical Serializers - API serialization for medical models.

Pre-implemented:
- PatientSerializer
- MedicationSerializer

TODO (Exercise): Implement PrescriptionSerializer
"""

from rest_framework import serializers

from .models import Medication, Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""

    class Meta:
        model = Patient
        fields = ["id", "first_name", "last_name", "birth_date", "status"]


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for Medication model."""

    class Meta:
        model = Medication
        fields = ["id", "code", "label", "status"]


# =============================================================================
# TODO: Implement PrescriptionSerializer here
# =============================================================================
#
# Requirements:
# - All Prescription fields
# - Nested patient/medication info for read operations
# - Validation: end_date >= start_date
#
# Example:
# class PrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescription
#         fields = "__all__"
# =============================================================================
