from django.forms import ModelForm

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
    def __init__(self, user, *args, **kwargs):
        super(ConsentForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = PatientConsent
        labels = {
            "operation": "Operation", "patient_name": "Patient Name", "patient_dob": "Patient Date of Birth",
            "inability": "Reason for Inability to Consent (if applicable)", "consent_video": "Consent Video",
            "relative_name": "Name of Alternative Consenter (if applicable)",
            "relationship_to_patient": "Alternative Consenter's Relationship to Patient (if applicable)"
        }
        
        fields = ['operation', 'patient_name', 'patient_dob', 'physician', 'nurse', 'inability', "relative_name",
                  "relationship_to_patient", "consent_video"]


class OperationForm(ModelForm):
    class Meta: 
        model = Operation
        fields = ['name', 'consent_form']
