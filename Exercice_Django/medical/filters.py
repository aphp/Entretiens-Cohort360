import django_filters

from .models import Patient, Medication, MedicationRequest


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
        fields = ["code", "label", "status"]


class MedicationRequestFilter(django_filters.FilterSet):
    patient = django_filters.NumberFilter(field_name="subject_id")
    medication = django_filters.NumberFilter(field_name="medication_reference_id")
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")

    date_start = django_filters.DateFilter(field_name="validity_period_start", lookup_expr="exact")
    date_start_after = django_filters.DateFilter(field_name="validity_period_start", lookup_expr="gte")
    date_start_before = django_filters.DateFilter(field_name="validity_period_start", lookup_expr="lte")

    date_end = django_filters.DateFilter(field_name="validity_period_end", lookup_expr="exact")
    date_end_after = django_filters.DateFilter(field_name="validity_period_end", lookup_expr="gte")
    date_end_before = django_filters.DateFilter(field_name="validity_period_end", lookup_expr="lte")

    class Meta:
        model = MedicationRequest
        fields = []
