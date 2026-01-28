from django import forms
import django_filters

class DateRangeForFilterWidget(django_filters.widgets.RangeWidget):
    """Widget pour rechercher dans une plage de dates."""
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets = [
            forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        ]
        
