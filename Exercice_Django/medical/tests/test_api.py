from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from medical.models import Patient, Medication, MedicationRequest


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


class MedicationRequestApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("medicationrequest-list")

        self.patient_a = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10",
        )
        self.patient_b = Patient.objects.create(
            last_name="Durand", first_name="Jean", birth_date="1980-05-20",
        )
        self.med_a = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF,
        )
        self.med_b = Medication.objects.create(
            code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_ACTIF,
        )

        self.mr1 = MedicationRequest.objects.create(
            subject=self.patient_a,
            medication_reference=self.med_a,
            validity_period_start=date(2025, 1, 1),
            validity_period_end=date(2025, 6, 30),
            status=MedicationRequest.STATUS_ACTIVE,
            note="Traitement initial",
        )
        self.mr2 = MedicationRequest.objects.create(
            subject=self.patient_b,
            medication_reference=self.med_b,
            validity_period_start=date(2025, 3, 1),
            validity_period_end=date(2025, 9, 30),
            status=MedicationRequest.STATUS_ON_HOLD,
        )

    # ── LIST ────────────────────────────────────────────────

    def test_list(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.json()), 2)

    def test_list_fhir_shape(self):
        r = self.client.get(self.url)
        item = r.json()[0]
        self.assertIn("subject", item)
        self.assertIn("reference", item["subject"])
        self.assertIn("display", item["subject"])
        self.assertIn("medicationReference", item)
        self.assertIn("validityPeriodStart", item)
        self.assertIn("validityPeriodEnd", item)
        self.assertIn("authoredOn", item)
        self.assertIn("status", item)

    # ── FILTERS ─────────────────────────────────────────────

    def test_filter_by_patient(self):
        r = self.client.get(self.url, {"patient": self.patient_a.pk})
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["subject"]["reference"], f"Patient/{self.patient_a.pk}")

    def test_filter_by_medication(self):
        r = self.client.get(self.url, {"medication": self.med_b.pk})
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["medicationReference"]["reference"], f"Medication/{self.med_b.pk}")

    def test_filter_by_status(self):
        r = self.client.get(self.url, {"status": "on-hold"})
        data = r.json()
        self.assertTrue(all(d["status"] == "on-hold" for d in data))
        self.assertEqual(len(data), 1)

    def test_filter_date_start_after(self):
        r = self.client.get(self.url, {"date_start_after": "2025-02-01"})
        self.assertEqual(len(r.json()), 1)

    def test_filter_date_end_before(self):
        r = self.client.get(self.url, {"date_end_before": "2025-07-01"})
        self.assertEqual(len(r.json()), 1)

    def test_filter_combined(self):
        r = self.client.get(self.url, {
            "patient": self.patient_a.pk,
            "status": "active",
            "date_start_after": "2024-01-01",
        })
        data = r.json()
        self.assertEqual(len(data), 1)

    # ── CREATE ──────────────────────────────────────────────

    def test_create_valid(self):
        payload = {
            "subject": self.patient_a.pk,
            "medicationReference": self.med_a.pk,
            "validityPeriodStart": "2025-10-01",
            "validityPeriodEnd": "2025-12-31",
            "status": "active",
            "note": "Nouveau traitement",
        }
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicationRequest.objects.count(), 3)

    def test_create_with_fhir_reference(self):
        payload = {
            "subject": {"reference": f"Patient/{self.patient_b.pk}"},
            "medicationReference": {"reference": f"Medication/{self.med_b.pk}"},
            "validityPeriodStart": "2025-10-01",
            "validityPeriodEnd": "2025-12-31",
            "status": "active",
        }
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_dates(self):
        payload = {
            "subject": self.patient_a.pk,
            "medicationReference": self.med_a.pk,
            "validityPeriodStart": "2025-12-31",
            "validityPeriodEnd": "2025-01-01",
            "status": "active",
        }
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("validityPeriodEnd", r.json())

    def test_create_missing_required_fields(self):
        r = self.client.post(self.url, {}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_nonexistent_patient(self):
        payload = {
            "subject": 99999,
            "medicationReference": self.med_a.pk,
            "validityPeriodStart": "2025-01-01",
            "validityPeriodEnd": "2025-06-01",
            "status": "active",
        }
        r = self.client.post(self.url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # ── UPDATE (PUT) ────────────────────────────────────────

    def test_update_put(self):
        url = reverse("medicationrequest-detail", args=[self.mr1.pk])
        payload = {
            "subject": self.patient_a.pk,
            "medicationReference": self.med_b.pk,
            "validityPeriodStart": "2025-01-01",
            "validityPeriodEnd": "2025-12-31",
            "status": "on-hold",
            "note": "Changement médicament",
        }
        r = self.client.put(url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.mr1.refresh_from_db()
        self.assertEqual(self.mr1.status, "on-hold")
        self.assertEqual(self.mr1.medication_reference_id, self.med_b.pk)

    # ── UPDATE (PATCH) ──────────────────────────────────────

    def test_partial_update(self):
        url = reverse("medicationrequest-detail", args=[self.mr1.pk])
        r = self.client.patch(url, {"status": "entered-in-error"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.mr1.refresh_from_db()
        self.assertEqual(self.mr1.status, "entered-in-error")

    def test_partial_update_invalid_dates(self):
        url = reverse("medicationrequest-detail", args=[self.mr1.pk])
        r = self.client.patch(url, {"validityPeriodEnd": "2024-01-01"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # ── DELETE interdit ─────────────────────────────────────

    def test_delete_not_allowed(self):
        url = reverse("medicationrequest-detail", args=[self.mr1.pk])
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
