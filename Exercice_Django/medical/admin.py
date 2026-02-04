from django.contrib import admin
from medical.models import Patient, Medication, Prescription


class PatientAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")


class MedicationAdmin(admin.ModelAdmin):
    list_display = ("code", "status", "label")


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "medication",
        "status",
        "patient_dob",
        "begin_date",
        "end_date",
    )

    def patient_dob(self, obj):
        return obj.patient.birth_date


admin.site.register(Patient, PatientAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
