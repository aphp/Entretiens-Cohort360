from rest_framework import serializers
from .models import Patient, Medication, MedicationRequest


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "last_name", "first_name", "birth_date"]


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ["id", "code", "label", "status"]


class FhirReferenceField(serializers.PrimaryKeyRelatedField):
    """Champ qui accepte un ID ou une référence FHIR en entrée,
    et produit une référence FHIR en sortie."""

    def __init__(self, resource_type, **kwargs):
        self.resource_type = resource_type
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if isinstance(data, dict) and "reference" in data:
            try:
                pk = int(data["reference"].split("/")[-1])
                return super().to_internal_value(pk)
            except (ValueError, IndexError):
                self.fail("incorrect_type", data_type=type(data).__name__)
        return super().to_internal_value(data)

    def to_representation(self, value):
        return {
            "reference": f"{self.resource_type}/{value.pk}",
            "display": str(value),
        }


class MedicationRequestSerializer(serializers.ModelSerializer):
    subject = FhirReferenceField(
        resource_type="Patient",
        queryset=Patient.objects.all(),
    )
    medicationReference = FhirReferenceField(
        resource_type="Medication",
        queryset=Medication.objects.all(),
        source="medication_reference",
    )
    validityPeriodStart = serializers.DateField(source="validity_period_start")
    validityPeriodEnd = serializers.DateField(source="validity_period_end")
    authoredOn = serializers.DateTimeField(source="authored_on", read_only=True)

    class Meta:
        model = MedicationRequest
        fields = [
            "id",
            "status",
            "subject",
            "medicationReference",
            "validityPeriodStart",
            "validityPeriodEnd",
            "note",
            "authoredOn",
        ]

    def validate(self, data):
        start = data.get("validity_period_start")
        end = data.get("validity_period_end")

        if self.instance:
            start = start or self.instance.validity_period_start
            end = end or self.instance.validity_period_end

        if start and end and end < start:
            raise serializers.ValidationError(
                {"validityPeriodEnd": "La date de fin doit être postérieure ou égale à la date de début."}
            )
        return data
