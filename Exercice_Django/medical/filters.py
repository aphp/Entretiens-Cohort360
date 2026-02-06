from django_filters import rest_framework as filters

from .models import Patient, Medication, Prescription


class PatientFilter(filters.FilterSet):
    nom = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    prenom = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    date_naissance = filters.DateFilter(field_name="birth_date")
    id = filters.CharFilter(method="filter_ids")

    def filter_ids(self, queryset, name, value):
        request = getattr(self, "request", None)
        values = []
        if request is not None:
            repeated = request.GET.getlist("id")
            for v in repeated:
                values.extend(v.split(","))
        if not values and value:
            values = value.split(",")
        ids = [int(v) for v in values if str(v).strip().isdigit()]
        return queryset.filter(id__in=ids) if ids else queryset

    class Meta:
        model = Patient
        fields = []


class MedicationFilter(filters.FilterSet):
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    label = filters.CharFilter(field_name="label", lookup_expr="icontains")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Medication
        fields = []


# TODO We should handle accented-letter-agnostic search to ease UX
# PM is aware: see ticket COHORT360-123456.
class PrescriptionFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    medication_code = filters.CharFilter(
        field_name="medication__code", lookup_expr="startswith"
    )
    medication_label = filters.CharFilter(
        field_name="medication__label", lookup_expr="icontains"
    )
    patient_firstname = filters.CharFilter(
        field_name="patient__first_name", lookup_expr="icontains"
    )
    patient_lastname = filters.CharFilter(
        field_name="patient__last_name", lookup_expr="icontains"
    )
    begin_date = filters.DateFromToRangeFilter(field_name="begin_date")
    begin_date_on = filters.DateFilter(field_name="begin_date")
    end_date = filters.DateFromToRangeFilter(field_name="end_date")
    end_date_on = filters.DateFilter(field_name="end_date")

    class Meta:
        model = Prescription
        fields = []
