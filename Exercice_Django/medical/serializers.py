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
    class Meta:
        model = Prescription
        fields = [
            "id",
            "patient",
            "medication",
            "dosage",
            "start_date",
            "end_date",
            "status",
        ]
        
    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        return attrs
