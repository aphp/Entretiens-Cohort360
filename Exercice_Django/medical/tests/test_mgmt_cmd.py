from unittest import TestCase as StdTestCase
from datetime import date
from medical.management.commands.seed_demo import (
    random_interval_between,
    Command as SeedDemoCommand,
)
from django.test import TestCase as DjangoTestCase
from django.core.management.base import CommandError

from medical.models import Patient, Medication


class RandomIntervalHelperTestCase(StdTestCase):
    def test_smoke(self):
        # arrange
        not_before = date(year=2020, month=4, day=6)
        not_after = date(year=2030, month=1, day=20)

        # act
        actual_from, actual_to = random_interval_between(not_before, not_after)

        # assert
        self.assertGreater(actual_from, not_before)
        self.assertGreater(actual_to, actual_from)
        self.assertGreater(not_after, actual_to)

    # TODO other tests, such as testing boundaries or unordered parameters


class SeedDemoCommandTestCase(DjangoTestCase):
    def setUp(self):
        self.sut = SeedDemoCommand()

    def test_validation_without_prescription(self):
        cases = [
            dict(n_patients=0, n_meds=0, keep_data=True),
            dict(n_patients=0, n_meds=0, keep_data=False),
            dict(n_patients=0, n_meds=1, keep_data=True),
            dict(n_patients=0, n_meds=1, keep_data=False),
            dict(n_patients=1, n_meds=0, keep_data=True),
            dict(n_patients=1, n_meds=0, keep_data=False),
            dict(n_patients=1, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=False),
        ]
        for single_case in cases:
            with self.subTest(**single_case):
                self.sut._validate_inputs(n_prescriptions=0, **single_case)

    def test_validation_with_prescription_and_no_existing_data_raise_expected(self):
        cases = [
            dict(n_patients=0, n_meds=0, keep_data=True),
            dict(n_patients=0, n_meds=0, keep_data=False),
            dict(n_patients=0, n_meds=1, keep_data=True),
            dict(n_patients=0, n_meds=1, keep_data=False),
            dict(n_patients=1, n_meds=0, keep_data=True),
            dict(n_patients=1, n_meds=0, keep_data=False),
        ]
        for single_case in cases:
            with self.subTest(**single_case):
                with self.assertRaises(CommandError):
                    self.sut._validate_inputs(n_prescriptions=1, **single_case)

    def test_validation_with_prescription_and_no_existing_data__ok(self):
        cases = [
            dict(n_patients=1, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=False),
        ]
        for single_case in cases:
            with self.subTest(**single_case):
                self.sut._validate_inputs(n_prescriptions=1, **single_case)

    def test_validation_with_prescription_and_existing_patient_raise_expected(self):
        cases = [
            dict(n_patients=0, n_meds=0, keep_data=True),
            dict(n_patients=0, n_meds=0, keep_data=False),
            dict(n_patients=1, n_meds=0, keep_data=True),
            dict(n_patients=1, n_meds=0, keep_data=False),
            dict(n_patients=0, n_meds=1, keep_data=False),
        ]
        Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        for single_case in cases:
            with self.subTest(**single_case):
                with self.assertRaises(CommandError):
                    self.sut._validate_inputs(n_prescriptions=1, **single_case)

    def test_validation_with_prescription_and_existing_patient__ok(self):
        cases = [
            dict(n_patients=0, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=False),
        ]
        Patient.objects.create(
            last_name="Martin", first_name="Jeanne", birth_date="1992-03-10"
        )
        for single_case in cases:
            with self.subTest(**single_case):
                self.sut._validate_inputs(n_prescriptions=1, **single_case)

    def test_validation_with_prescription_and_existing_medication_raise_expected(self):
        cases = [
            dict(n_patients=0, n_meds=0, keep_data=False),
            dict(n_patients=0, n_meds=0, keep_data=True),
            dict(n_patients=0, n_meds=1, keep_data=False),
            dict(n_patients=0, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=0, keep_data=False),
        ]
        Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        for single_case in cases:
            with self.subTest(**single_case):
                with self.assertRaises(CommandError):
                    self.sut._validate_inputs(n_prescriptions=1, **single_case)

    def test_validation_with_prescription_and_existing_medication__ok(self):
        cases = [
            dict(n_patients=1, n_meds=0, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=True),
            dict(n_patients=1, n_meds=1, keep_data=False),
        ]
        Medication.objects.create(
            code="PARA500", label="Paracétamol 500mg", status=Medication.STATUS_ACTIF
        )
        for single_case in cases:
            with self.subTest(**single_case):
                self.sut._validate_inputs(n_prescriptions=1, **single_case)
