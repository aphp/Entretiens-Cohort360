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
        # TODO could be shortened to 5 to reclaim DB space
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIF,
    )

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"{self.code} - {self.label} ({self.status})"


class Prescription(models.Model):
    """Représente une prescription"""

    STATUS_VALIDE = "valide"
    STATUS_EN_ATTENTE = "en_attente"
    STATUS_SUPPR = "suppr"
    STATUS_CHOICES = (
        (STATUS_VALIDE, "valide"),
        (STATUS_SUPPR, "suppr"),
        (STATUS_EN_ATTENTE, "en_attente"),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, null=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_VALIDE
    )
    begin_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    comment = models.CharField(max_length=1000, null=False, blank=True)
