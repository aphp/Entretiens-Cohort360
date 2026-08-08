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
    """Représente une prescription médicale."""

    STATUS_VALID = "valide"
    STATUS_ATTENTE = "en_attente"
    STATUS_SUPPR = "suppr"
    STATUS_CHOICES = (
        (STATUS_VALID, "valide"),
        (STATUS_ATTENTE , "en_attente"),
        (STATUS_SUPPR, "suppr"),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions", null=False, blank=False)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name="prescriptions", null=False, blank=False)
    prescription_start_date = models.DateField( null=False, blank=False)
    prescription_end_date = models.DateField(null=False, blank=False)
    presscription_status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_VALID)
    commentaire = models.TextField(null=True, blank=True)

    def clean(self):
        """Validation personnalisée pour vérifier les dates."""
        super().clean()
        if self.prescription_end_date < self.prescription_start_date:
            raise ValidationError({
                'prescription_end_date': "La date de fin doit être supérieure ou égale à la date de début."
            })
    class Meta:
        ordering = ["patient", "medication", "prescription_start_date"]

    def __str__(self) -> str:  # pragma: no cover - simple repr
        return f"Prescription num: {self.id} de {self.medication} pour {self.patient} du {self.prescription_start_date.strftime('%d/%m/%Y')} au {self.prescription_end_date.strftime('%d/%m/%Y')} ({self.presscription_status})"