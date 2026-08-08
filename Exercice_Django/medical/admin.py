from django.contrib import admin
from .models import Patient, Medication, Prescription


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "birth_date")
    search_fields = ("last_name", "first_name")


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "label", "status")
    search_fields = ("code", "label")
    list_filter = ("status",)


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "medication",
        "dosage",
        "start_date",
        "end_date",
        "status",
    )
    list_filter = ("status", "start_date")
    search_fields = ("patient__last_name", "medication__label")