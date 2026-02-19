from django.core.exceptions import ValidationError
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
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_ACTIF)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.code} - {self.label} ({self.status})"


class MedicationRequest(models.Model):
    """FHIR R4 MedicationRequest — prescription médicamenteuse."""

    STATUS_ACTIVE = "active"
    STATUS_ON_HOLD = "on-hold"
    STATUS_ENTERED_IN_ERROR = "entered-in-error"
    STATUS_CHOICES = (
        (STATUS_ACTIVE, "active"),
        (STATUS_ON_HOLD, "on-hold"),
        (STATUS_ENTERED_IN_ERROR, "entered-in-error"),
    )

    subject = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medication_requests",
    )
    medication_reference = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name="medication_requests",
    )
    validity_period_start = models.DateField()
    validity_period_end = models.DateField()
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    note = models.TextField(blank=True, default="")
    authored_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-authored_on", "id"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"MedicationRequest/{self.pk} — {self.subject} / {self.medication_reference}"

    def clean(self):
        if (
            self.validity_period_start
            and self.validity_period_end
            and self.validity_period_end < self.validity_period_start
        ):
            raise ValidationError(
                {"validity_period_end": "La date de fin doit être postérieure ou égale à la date de début."}
            )
