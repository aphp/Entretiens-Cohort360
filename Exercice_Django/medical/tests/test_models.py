from django.test import TestCase
from django.core.management import call_command
from datetime import date
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from medical.models import Patient, Medication, Prescription


class PrescriptionModelTestCase(TestCase):
    def _create_patients(self, count=1):
        call_command(
            "seed_demo",
            "-k",
            f"--patients={count}",
            "--medications=0",
            "--prescriptions=0",
        )

    def _create_medications(self, count=1):
        call_command(
            "seed_demo",
            "-k",
            "--patients=0",
            f"--medications={count}",
            "--prescriptions=0",
        )

    def _create_prescriptions(self, count=1):
        call_command(
            "seed_demo",
            "-k",
            "--patients=0",
            "--medications=0",
            f"--prescriptions={count}",
        )

    def test_save__smoke(self):
        # arrange
        self._create_patients(1)
        self._create_medications(1)
        patient = Patient.objects.first()
        medication = Medication.objects.first()
        prescription_begins_on = date(2020, 1, 1)
        prescription_ends_on = date(2020, 2, 1)

        # act
        prescription = Prescription.objects.create(
            patient=patient,
            medication=medication,
            begin_date=prescription_begins_on,
            end_date=prescription_ends_on,
        )

        # assert
        self.assertTrue(Prescription.objects.filter(id=prescription.id).exists())

    def test_save__fails_for_bad_dates(self):
        """prescription ends before it begins"""
        # arrange
        self._create_patients(1)
        self._create_medications(1)
        patient = Patient.objects.first()
        medication = Medication.objects.first()
        prescription_begins_on = date(2050, 12, 31)
        prescription_ends_on = date(2020, 2, 1)

        # act & assert
        with self.assertRaises(ValidationError) as em:
            Prescription.objects.create(
                patient=patient,
                medication=medication,
                begin_date=prescription_begins_on,
                end_date=prescription_ends_on,
            )
        self.assertEqual(em.exception.message, "unordered prescription dates")

    def test_save__fails_for_missing_patient(self):
        """prescription ends before it begins"""
        # arrange
        self._create_medications(1)
        patient = None
        medication = Medication.objects.first()
        prescription_begins_on = date(2020, 1, 1)
        prescription_ends_on = date(2020, 2, 1)

        # act & assert
        with self.assertRaises(IntegrityError) as em:
            Prescription.objects.create(
                patient=patient,
                medication=medication,
                begin_date=prescription_begins_on,
                end_date=prescription_ends_on,
            )

    def test_save__fails_for_missing_medication(self):
        """prescription ends before it begins"""
        # arrange
        self._create_patients(1)
        patient = Patient.objects.first()
        medication = None
        prescription_begins_on = date(2020, 1, 1)
        prescription_ends_on = date(2020, 2, 1)

        # act & assert
        with self.assertRaises(IntegrityError) as em:
            Prescription.objects.create(
                patient=patient,
                medication=medication,
                begin_date=prescription_begins_on,
                end_date=prescription_ends_on,
            )
