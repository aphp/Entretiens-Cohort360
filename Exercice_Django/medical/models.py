from django import forms
from django.db import models


class Patient(models.Model):
    """Représente un patient."""

    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name", "id"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.last_name} {self.first_name}"


class Medication(models.Model):
    """Représente un médicament."""

    STATUS_ACTIF = "actif"
    STATUS_SUPPR = "suppr"
    STATUS_CHOICES = (
        (STATUS_ACTIF, "actif"),
        (STATUS_SUPPR, "suppr"),
    )

    code = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=255)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=STATUS_ACTIF)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.code} - {self.label} ({self.status})"


class Prescription(models.Model):
    """Represent a prescription."""

    STATUS_VALID = "valide"
    STATUS_WAITING = "en attente"
    STATUS_SUPPR = "suppr"
    STATUS_CHOICES = (
        (STATUS_VALID, "valide"),
        (STATUS_WAITING, "attente"),
        (STATUS_SUPPR, "suppr"),
    )

    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE)
    medication = models.OneToOneField(
        Medication, on_delete=models.CASCADE)
    starting_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=STATUS_VALID)
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["status", "starting_date"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.code} - {self.label} ({self.status})"

    def clean(self):
        super().clean()
        if not (self.starting_date <= self.end_date):
            raise forms.ValidationError('Invalid start and end datetime')
