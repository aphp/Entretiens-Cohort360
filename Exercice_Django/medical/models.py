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
    
    
class Prescription(models.Model):
    """Représente une prescription médicamenteuse."""

    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, "active"),
        (STATUS_COMPLETED, "completed"),
        (STATUS_CANCELLED, "cancelled"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="prescriptions",
    )

    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT,
        related_name="prescriptions",
    )

    dosage = models.CharField(max_length=150)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )

    class Meta:
        ordering = ["-start_date", "id"]

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            from django.core.exceptions import ValidationError
            raise ValidationError("End date must be after start date.")

    def __str__(self) -> str:  # pragma: no cover
        return f"Prescription #{self.id} - {self.patient}"
