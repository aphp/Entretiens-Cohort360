import django_filters
from django import forms
from .models import Patient, Medication, Prescription
from.widgets import DateRangeForFilterWidget

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

class PrescriptionFilter(django_filters.FilterSet):
    nom=django_filters.CharFilter(field_name="patient__last_name", lookup_expr="icontains", label="Nom Patient",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom Patient'
        })
    )    
    medication=django_filters.CharFilter(
        field_name="medication__code",
        lookup_expr="exact",
        label="Code Médicament",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'code Medicament'
        })
    )
    status = django_filters.ChoiceFilter(
        field_name='presscription_status',
        choices=Prescription.STATUS_CHOICES,
        lookup_expr='exact',
        label="Statut",
        empty_label="- Tout -",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    active_period = django_filters.DateFromToRangeFilter(
        field_name='prescription_start_date',
        widget=DateRangeForFilterWidget(),
        label="Période d'activité"
    )
    class Meta:
        model = Prescription
        fields = ['nom', 'medication', 'status', 'active_period']