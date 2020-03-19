from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

CONSENT_STATUS = (
    (1, "Consent given by patient"),
    (2, "Consent given by guardian/relative (see relationship)"),
    (3, "Inability to give consent (see reason)"),
)


class Operation(models.Model):
    consent_form = models.FileField(upload_to="forms/")
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class PatientConsent(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.DO_NOTHING)
    patient_name = models.CharField(max_length=256)
    patient_dob = models.DateField()
    today_date = models.DateField(default=timezone.now)
    consent_status = models.IntegerField(choices=CONSENT_STATUS, default=1)
    physician = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="physician", null=True)
    physician_signature = models.BooleanField(default=False)
    nurse = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="nurse", null=True, blank=True)
    nurse_signature = models.BooleanField(default=False)
    consent_video = models.FileField(upload_to="videos/")
    password = models.CharField(max_length=32, null=True)
    relationship_to_patient = models.CharField(max_length=32, default="self")
    relative_name = models.CharField(max_length=256, blank=True)
    inability = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.patient_name} on {self.today_date} for {self.operation}"
