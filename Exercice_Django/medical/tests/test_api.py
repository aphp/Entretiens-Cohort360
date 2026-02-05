from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from medical.models import Patient, Medication, Prescription

# FIXME All tests that `assertGreaterEqual` should be `assertEqual` because
# the test db is expected to be empty when firing each test class. If not,
# fix that first.


class ApiListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Patients
        jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        jean = Patient.objects.create(
            last_name="Durand", first_name="Jean", birth_date="1980-05-20"
        )
        bernard = Patient.objects.create(last_name="Bernard", first_name="Paul")

        # Medications
        paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        ibuprofène = Medication.objects.create(
            code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_SUPPR
        )

        # Prescriptions
        Prescription.objects.create(
            patient=jeanne,
            medication=paracétamol,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        Prescription.objects.create(
            patient=jean,
            medication=ibuprofène,
            status=Prescription.STATUS_EN_ATTENTE,
            begin_date="2024-01-01",
            end_date="2024-12-31",
            comment="migraine",
        )

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

    def test_prescription_list(self):
        url = reverse("prescription-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_prescription_filter_status_valide(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"status": "valide"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_status_suppr(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"status": "suppr"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_medication_code_starts_with(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"medication_code": "PARA5"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_medication_code_contains(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"medication_code": "RA5"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_medication_label_contains_uppercase(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"medication_label": "PROF"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_medication_label_contains_lowercase(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"medication_label": "prof"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_patient_firstname_contains(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"patient_firstname": "jean"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_prescription_filter_patient_firstname_not_contains(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"patient_firstname": "xyz"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_patient_lastname_contains(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"patient_lastname": "DURAND"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_patient_lastname_not_contains(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"patient_lastname": "xyz"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_begin_date_on_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_on": "1920-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_begin_date_on_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_on": "2020-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_begin_date_before_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_before": "1920-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_begin_date_before_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_before": "2026-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_prescription_filter_begin_date_after_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_after": "2030-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_begin_date_after_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"begin_date_after": "2023-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_end_date_on_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_on": "1920-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_end_date_on_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_on": "2024-12-31"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_filter_end_date_before_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_before": "1920-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_end_date_before_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_before": "2026-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

    def test_prescription_filter_end_date_after_no_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_after": "2030-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_prescription_filter_end_date_after_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(url, {"end_date_after": "2023-01-01"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_prescription_combined_with_result(self):
        url = reverse("prescription-list")
        r = self.client.get(
            url, {"end_date_after": "2000-01-01", "patient_firstname": "jeanne"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)
