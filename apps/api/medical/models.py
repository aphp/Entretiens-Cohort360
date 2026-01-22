"""
Medical Models - Base entities for the healthcare application.

This module contains the core models that are pre-implemented:
- Patient: Healthcare patient records
- Medication: Available medications

TODO (Exercise): Implement the Prescription model
See docs/exercises/django/README.md for specifications.
"""

from django.db import models


class Patient(models.Model):
    """Patient model representing healthcare patients."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("actif", "Actif"), ("suppr", "Supprimé")],
        default="actif",
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"


class Medication(models.Model):
    """Medication model representing available medications."""

    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=[("actif", "Actif"), ("suppr", "Supprimé")],
        default="actif",
    )

    class Meta:
        ordering = ["label"]

    def __str__(self) -> str:
        return f"{self.code} - {self.label}"


# =============================================================================
# TODO: Implement Prescription model here
# =============================================================================
#
# Requirements (from docs/exercises/django/README.md):
# - ForeignKey to Patient (required)
# - ForeignKey to Medication (required)
# - start_date: Date (required)
# - end_date: Date (required)
# - status: choices ["valide", "en_attente", "suppr"]
# - comment: TextField (optional)
#
# Constraints:
# - end_date >= start_date
#
# Example:
# class Prescription(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
#     ...
# =============================================================================
