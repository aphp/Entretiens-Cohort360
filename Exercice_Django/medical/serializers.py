from rest_framework import serializers
from .models import Patient, Medication, Prescription


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "last_name", "first_name", "birth_date"]


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "code", "label", "status"]

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.__str__", read_only=True)
    medication_code = serializers.CharField(source="medication.code", read_only=True)
    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "medication",
            "patient_name",
            "medication_code",
            "prescription_start_date",
            "prescription_end_date",
            "presscription_status",
            "commentaire"
        ]
    def validate(self, data):
        """Validation pour vérifier les dates."""
        start_date = data.get("prescription_start_date")
        end_date = data.get("prescription_end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                "prescription_end_date": "La date de fin de prescription doit être supérieure ou égale à la date de début de prescription."
            })

        return data