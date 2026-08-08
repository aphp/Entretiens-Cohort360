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
    patient_name = serializers.SerializerMethodField()
    medication_label = serializers.CharField(
        source="medication.label", read_only=True
    )

    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "patient_name",
            "medication",
            "medication_label",
            "dosage",
            "start_date",
            "end_date",
            "status",
        ]

    def get_patient_name(self, obj):
        return f"{obj.patient.last_name} {obj.patient.first_name}"

    def validate(self, data):
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        return data
