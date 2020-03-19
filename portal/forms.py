from django import forms
from .models import Institution


class InstitutionForm(forms.Form):
    institution = forms.ModelChoiceField(Institution.objects)
