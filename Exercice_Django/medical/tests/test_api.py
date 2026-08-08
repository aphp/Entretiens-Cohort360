from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from medical.models import Patient, Medication, Prescription


class ApiListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Patients
        Patient.objects.create(last_name="Martin", first_name="Jeanne", birth_date="1992-03-10")
        Patient.objects.create(last_name="Durand", first_name="Jean", birth_date="1980-05-20")
        Patient.objects.create(last_name="Bernard", first_name="Paul")

        # Medications
        Medication.objects.create(code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF)
        Medication.objects.create(code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_SUPPR)

    def test_patient_list(self):
        url = reverse("patient-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 3)

    def test_patient_filter_nom(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"nom": "mart"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(all("mart" in p["last_name"].lower() for p in data))

    def test_patient_filter_date(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"date_naissance": "1980-05-20"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(all(p["birth_date"] == "1980-05-20" for p in data))

    def test_medication_list(self):
        url = reverse("medication-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 2)

    def test_medication_filter_status(self):
        url = reverse("medication-list")
        r = self.client.get(url, {"status": "actif"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(all(m["status"] == "actif" for m in data))
        

class PrescriptionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.patient = Patient.objects.create(
            last_name="Martin",
            first_name="Jean",
        )

        self.medication = Medication.objects.create(
            code="MED001",
            label="Doliprane",
            status=Medication.STATUS_ACTIF,
        )

    def test_create_prescription(self):
        url = reverse("prescription-list")

        data = {
            "patient": self.patient.id,
            "medication": self.medication.id,
            "dosage": "500mg",
            "start_date": "2025-01-01",
            "status": "active",
        }

        r = self.client.post(url, data)

        self.assertEqual(r.status_code, 201)
        self.assertEqual(Prescription.objects.count(), 1)

    def test_filter_prescription_by_patient(self):
        Prescription.objects.create(
            patient=self.patient,
            medication=self.medication,
            dosage="500mg",
            start_date="2025-01-01",
            status="active",
        )

        url = reverse("prescription-list")
        r = self.client.get(url, {"patient": self.patient.id})

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_invalid_end_date(self):
        url = reverse("prescription-list")

        data = {
            "patient": self.patient.id,
            "medication": self.medication.id,
            "dosage": "500mg",
            "start_date": "2025-01-10",
            "end_date": "2025-01-01",
            "status": "active",
        }

        r = self.client.post(url, data)

        self.assertEqual(r.status_code, 400)
