"""
Medical API Tests.

Pre-implemented tests for Patient and Medication APIs.

TODO (Exercise): Add Prescription API tests
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from medical.models import Medication, Patient


class PatientAPITests(APITestCase):
    """Tests for the Patient API."""

    def setUp(self):
        """Set up test data."""
        self.patient1 = Patient.objects.create(
            first_name="Jean",
            last_name="Dupont",
            birth_date="1980-01-15",
            status="actif",
        )
        self.patient2 = Patient.objects.create(
            first_name="Marie",
            last_name="Martin",
            birth_date="1990-06-20",
            status="actif",
        )

    def test_list_patients(self):
        """Test listing all patients."""
        response = self.client.get("/Patient/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_by_last_name(self):
        """Test filtering patients by last name."""
        response = self.client.get("/Patient/?last_name=Dupont")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["last_name"], "Dupont")

    def test_filter_by_nom(self):
        """Test filtering patients by French field name 'nom'."""
        response = self.client.get("/Patient/?nom=Martin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_patient_detail(self):
        """Test getting a single patient."""
        response = self.client.get(f"/Patient/{self.patient1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Jean")


class MedicationAPITests(APITestCase):
    """Tests for the Medication API."""

    def setUp(self):
        """Set up test data."""
        self.med1 = Medication.objects.create(
            code="MED001",
            label="Paracetamol 500mg",
            status="actif",
        )
        self.med2 = Medication.objects.create(
            code="MED002",
            label="Ibuprofene 400mg",
            status="actif",
        )

    def test_list_medications(self):
        """Test listing all medications."""
        response = self.client.get("/Medication/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_filter_by_code(self):
        """Test filtering medications by code."""
        response = self.client.get("/Medication/?code=MED001")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_status(self):
        """Test filtering medications by status."""
        response = self.client.get("/Medication/?status=actif")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)


# =============================================================================
# TODO: Implement Prescription API tests
# =============================================================================
#
# Test cases to implement:
# - test_list_prescriptions
# - test_create_prescription
# - test_update_prescription
# - test_filter_by_patient
# - test_filter_by_medication
# - test_filter_by_status
# - test_filter_by_date_range
# - test_validation_end_date_after_start_date
# =============================================================================
