import mimetypes

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.forms import ModelForm, Form, FileField, TextInput

from .models import PatientConsent, Operation


class ConsentForm(ModelForm):
    class Meta:
        model = PatientConsent
        fields = [
            "consent_type", "patient_name", "patient_dob", "patient_mrn", "attending_physician", "consenting_physician",
            "witness_name", "procedure", "diagnosis", "risk_ben_alt", "anesthesia_type", "ability_to_consent",
            "inability_reason", "representative_name", "relationship_to_patient"
            ]
        labels = {
            "risk_ben_alt": "Risks, Benefits, and Alternatives",
            "anesthesia_type": "Type of Anesthesia",
            "ability_to_consent": "Is the patient able to consent?",
            "inability_reason": "Reason for Inability to Consent",
            "representative_name": "Patient Representative Name"
        }
        widgets = {
            'patient_dob': TextInput(attrs={'type': 'date'})
        }


class OperationForm(ModelForm):
    class Meta: 
        model = Operation
        fields = ['name', 'consent_form']
        widgets = {
            'name': TextInput(attrs={'margin': 100}),
        }


class SignatureForm(Form):
    signature = FileField(validators=[FileExtensionValidator(allowed_extensions=['mov', 'mp4', 'png'])])


class ConsentFormAuthorization(ModelForm):
    password = forms.CharField(
        label="Password to view form",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = PatientConsent
        fields = ()

    def clean_password(self):
        if not check_password(self.cleaned_data["password"], self.instance.password_hash):
            raise ValidationError("Incorrect password")
        return self.cleaned_data["password"]
