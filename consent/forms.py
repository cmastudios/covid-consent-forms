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


class OperationForm(ModelForm):
    class Meta: 
        model = Operation
        fields = ['name', 'consent_form']
        widgets = {
            'name': TextInput(attrs={'margin': 100}),
        }


class SignatureForm(Form):
    signature = FileField()