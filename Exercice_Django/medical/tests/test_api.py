from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from random import randint

from medical.models import Patient, Medication, Prescription

# FIXME All tests that `assertGreaterEqual` should be `assertEqual` because
# the test db is expected to be empty when firing each test class. If not,
# fix that first.


class ApiRetrieveTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_patient_missing(self):

        url = reverse("patient-detail", args=(randint(0, 1000),))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json(), {"detail": "No Patient matches the given query."})

    def test_get_patient_exists(self):
        patient = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )

        url = reverse("patient-detail", args=(patient.id,))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "last_name": "Martin",
                "first_name": "Jeanne",
                "birth_date": "1992-03-10",
            },
        )

    def test_get_medication_missing(self):

        url = reverse("medication-detail", args=(randint(0, 1000),))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json(), {"detail": "No Medication matches the given query."})

    def test_get_medication_exists(self):
        medication = paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        url = reverse("medication-detail", args=(medication.id,))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "code": "PARA500",
                "label": "Paracétamol 500mg",
                "status": "actif",
            },
        )

    def test_get_prescription_missing(self):

        url = reverse("prescription-detail", args=(randint(0, 1000),))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            r.json(), {"detail": "No Prescription matches the given query."}
        )

    def test_get_prescription_exists(self):

        jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        prescription = Prescription.objects.create(
            patient=jeanne,
            medication=paracétamol,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )

        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 1,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )


class ApiCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        self.paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )

    def test_create_valid(self):
        url = reverse("prescription-list")
        r = self.client.post(
            url,
            {
                "patient": self.jeanne.id,
                "medication": self.paracétamol.id,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )
        self.assertEqual(r.status_code, 201)
        reponse_content = r.json()
        self.assertTrue(Prescription.objects.filter(id=reponse_content["id"]).exists())

    def test_create_unknown_patient(self):
        url = reverse("prescription-list")
        r = self.client.post(
            url,
            {
                "patient": randint(0, 1000),
                "medication": self.paracétamol.id,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )
        self.assertEqual(r.status_code, 400)
        self.assertIn("patient", r.json())

    def test_create_unknown_medication(self):
        url = reverse("prescription-list")
        r = self.client.post(
            url,
            {
                "patient": self.jeanne.id,
                "medication": randint(0, 1000),
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )
        self.assertEqual(r.status_code, 400)
        self.assertIn("medication", r.json())

    def test_create_out_of_order_dates(self):
        url = reverse("prescription-list")
        r = self.client.post(
            url,
            {
                "patient": self.jeanne.id,
                "medication": self.paracétamol.id,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "1982-12-31",
                "comment": "hypocondrie",
            },
        )
        self.assertEqual(r.status_code, 400)
        self.assertIn("unordered prescription dates", r.json())


class ApiCompleteUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )

        self.bernard = Patient.objects.create(last_name="Bernard", first_name="Paul")

        self.paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )

        self.ibuprofène = Medication.objects.create(
            code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_SUPPR
        )

    def test_put_prescription_missing(self):

        url = reverse("prescription-detail", args=(randint(0, 1000),))
        r = self.client.put(url, {})
        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            r.json(), {"detail": "No Prescription matches the given query."}
        )

    def test_put_prescription_ok(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.put(
            url,
            {
                "id": 1,
                "patient": self.bernard.id,
                "medication": self.paracétamol.id,
                "status": "en_attente",
                "begin_date": "2018-01-01",
                "end_date": "2019-12-31",
                "comment": "blabla",
            },
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": self.bernard.id,
                "medication": self.paracétamol.id,
                "status": "en_attente",
                "begin_date": "2018-01-01",
                "end_date": "2019-12-31",
                "comment": "blabla",
            },
        )


class ApiPartialUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )

        self.bernard = Patient.objects.create(last_name="Bernard", first_name="Paul")

        self.paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )

        self.ibuprofène = Medication.objects.create(
            code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_SUPPR
        )

    def test_patch_prescription_missing(self):

        url = reverse("prescription-detail", args=(randint(0, 1000),))
        r = self.client.patch(url, {})
        self.assertEqual(r.status_code, 404)
        self.assertEqual(
            r.json(), {"detail": "No Prescription matches the given query."}
        )

    def test_patch_prescription_comment_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"comment": "blabla"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 2,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "blabla",
            },
        )

    def test_patch_prescription_existing_patient_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"patient": self.bernard.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 2,
                "medication": 2,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )

    def test_patch_prescription_missing_patient_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"patient": randint(0, 1000)})
        self.assertEqual(r.status_code, 400)
        self.assertIn("patient", r.json())

    def test_patch_prescription_existing_medication_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"medication": self.paracétamol.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 1,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )

    def test_patch_prescription_missing_medication_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"medication": randint(0, 1000)})
        self.assertEqual(r.status_code, 400)
        self.assertIn("medication", r.json())

    def test_patch_prescription_begindate_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"begin_date": "2020-01-02"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 2,
                "status": "valide",
                "begin_date": "2020-01-02",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )

    def test_patch_prescription_enddate_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"end_date": "2023-01-22"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 2,
                "status": "valide",
                "begin_date": "2020-01-01",
                "end_date": "2023-01-22",
                "comment": "hypocondrie",
            },
        )

    def test_patch_prescription_out_of_order_dates(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"end_date": "1956-01-22"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("unordered prescription dates", r.json())

    def test_patch_prescription_status_update(self):
        prescription = Prescription.objects.create(
            patient=self.jeanne,
            medication=self.ibuprofène,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        url = reverse("prescription-detail", args=(prescription.id,))
        r = self.client.patch(url, {"status": "en_attente"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "id": 1,
                "patient": 1,
                "medication": 2,
                "status": "en_attente",
                "begin_date": "2020-01-01",
                "end_date": "2022-12-31",
                "comment": "hypocondrie",
            },
        )


class ApiListTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Patients
        self.jeanne = Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        self.jean = Patient.objects.create(
            last_name="Durand", first_name="Jean", birth_date="1980-05-20"
        )
        self.bernard = Patient.objects.create(last_name="Bernard", first_name="Paul")

        # Medications
        paracétamol = Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        ibuprofène = Medication.objects.create(
            code="IBU200", label="Ibuprofène 200mg", status=Medication.STATUS_SUPPR
        )

        # Prescriptions
        Prescription.objects.create(
            patient=self.jeanne,
            medication=paracétamol,
            status=Prescription.STATUS_VALIDE,
            begin_date="2020-01-01",
            end_date="2022-12-31",
            comment="hypocondrie",
        )
        Prescription.objects.create(
            patient=self.jean,
            medication=ibuprofène,
            status=Prescription.STATUS_EN_ATTENTE,
            begin_date="2024-01-01",
            end_date="2024-12-31",
            comment="migraine",
        )

    def test_patient_list_all(self):
        url = reverse("patient-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 3)

    def test_patient_filter_by_id_simple(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"id": self.bernard.id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_patient_filter_by_id_and_remove_non_id(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"id": f"a,{self.bernard.id}"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_patient_filter_by_id_and_remove_whitespaces(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"id": f"  {self.bernard.id}\t"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 1)

    def test_patient_filter_by_ids(self):
        url = reverse("patient-list")
        r = self.client.get(url, {"id": f"{self.bernard.id},{self.jeanne.id}"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)

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
