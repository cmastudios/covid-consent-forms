from django.forms import ModelForm, Form, FileField

from .models import PatientConsent, Operation


# patient_name = models.CharField(max_length=256)
# patient_dob = models.DateField()
# today_date = models.DateField()
# consent_status = models.IntegerField(choices=CONSENT_STATUS)
# physician = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="physician")
# nurse = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="nurse")
# consent_video = models.FileField(upload_to="videos/")
# password = models.CharField(max_length=32)
# relationship_to_patient = models.CharField(max_length=32)
# inability = models.CharField(max_length=256)
# proceedure_name = models.CharField(max_length=256)

class ConsentForm(ModelForm):
    class Meta:
        model = PatientConsent
        fields = [
            "consent_type", "patient_name", "patient_dob", "patient_mrn", "attending_physician", "consenting_physician", "witness_name", "procedure", "diagnosis", "risk_ben_alt", "anesthsia_type"
            ]
        labels = {
            "risk_ben_alt": "Risks, Benefits, and Alternatives",
            "anesthsia_type": "Type of Anesthesia"
        }

class OperationForm(ModelForm):
    class Meta: 
        model = Operation
        fields = ['name', 'consent_form']


class SignatureForm(Form):
    signature = FileField()