from django.contrib import admin
from medical.models import Patient, Medication


class PatientAdmin(admin.ModelAdmin):
    pass


class MedicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Patient, PatientAdmin)
admin.site.register(Medication, MedicationAdmin)
