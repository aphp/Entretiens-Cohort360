import django_filters

from .models import Patient, Medication, Prescription


class PatientFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    prenom = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    date_naissance = django_filters.DateFilter(field_name="birth_date")
    id = django_filters.CharFilter(method="filter_ids")

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


class MedicationFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(field_name="code", lookup_expr="icontains")
    label = django_filters.CharFilter(field_name="label", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Medication
        fields = []


# TODO We should handle accented-letter-agnostic search to ease UX
# PM is aware: see ticket COHORT360-123456.
class PrescriptionFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    medication_code = django_filters.CharFilter(
        field_name="medication__code", lookup_expr="startswith"
    )
    medication_label = django_filters.CharFilter(
        field_name="medication__label", lookup_expr="icontains"
    )
    patient_firstname = django_filters.CharFilter(
        field_name="patient__first_name", lookup_expr="icontains"
    )
    patient_lastname = django_filters.CharFilter(
        field_name="patient__last_name", lookup_expr="icontains"
    )
    begin_date = django_filters.DateFromToRangeFilter(field_name="begin_date")
    begin_date_on = django_filters.DateFilter(field_name="begin_date")
    end_date = django_filters.DateFromToRangeFilter(field_name="end_date")
    end_date_on = django_filters.DateFilter(field_name="end_date")

    class Meta:
        model = Prescription
        fields = []
