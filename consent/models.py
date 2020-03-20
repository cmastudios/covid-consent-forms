import mimetypes
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

CONSENT_STATUS = (
    (1, "Consent given by patient"),
    (2, "Consent given by guardian/relative (see relationship)"),
    (3, "Inability to give consent (see reason)"),
)

ANESTHESIA_TYPE = (
    (1, "General Anesthesia"),
    (2, "Local Anesthesia"),
    (3, "Sedation"),
    (4, "No Anesthesia")
)

ABLE_TO_CONSENT = {
    (1, "Yes"),
    (2, "No")
}


class Operation(models.Model):
    consent_form = models.FileField(upload_to="forms/")
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class PatientConsent(models.Model):
    consent_type = models.ForeignKey(Operation, on_delete=models.DO_NOTHING)

    patient_name = models.CharField(max_length=256)
    patient_dob = models.DateField()
    patient_mrn = models.CharField(max_length=64)

    # deals with physician's signature
    attending_physician = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="attending_physician")
    consenting_physician = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="consenting_physician")
    physician_signature = models.FileField(upload_to="videos/", null=True, blank=True)

    procedure = models.CharField(max_length=512)
    diagnosis = models.CharField(max_length=256)
    risk_ben_alt = models.CharField(max_length=4096)
    anesthesia_type = models.IntegerField(choices=ANESTHESIA_TYPE, default=4)

    # deals with patient's (or other)'s signature
    patient_signature = models.FileField(upload_to="videos/", null=True, blank=True)
    ability_to_consent = models.IntegerField(choices=ABLE_TO_CONSENT, default=1)
    inability_reason = models.CharField(max_length=256, null=True, blank=True)
    representative_name = models.CharField(max_length=256, null=True, blank=True)
    relationship_to_patient = models.CharField(max_length=256)

    # deals with nurse's signature
    witness_name = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="witness")
    witness_signature = models.FileField(upload_to="videos/", null=True, blank=True)

    today_date = models.DateTimeField(default=timezone.now)
    password = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.today_date} :: {self.patient_name}"

    @property
    def has_patient_signature(self):
        return self.patient_signature is not None and self.patient_signature != ""

    @property
    def has_physician_signature(self):
        return self.physician_signature is not None and self.physician_signature != ""

    @property
    def has_witness_signature(self):
        return self.witness_signature is not None and self.witness_signature != ""

    @property
    def has_any_signature(self):
        return self.has_witness_signature or self.has_physician_signature or self.has_patient_signature

    @property
    def has_inability_reason(self):
        return self.inability_reason is not None and self.inability_reason != ""

    @property
    def has_relative(self):
        return self.representative_name is not None and self.representative_name != ""

    @property
    def patient_signature_file_mime(self):
        return mimetypes.MimeTypes().guess_type(self.patient_signature.path)[0] if self.has_patient_signature else ""

    @property
    def physician_signature_file_mime(self):
        return mimetypes.MimeTypes().guess_type(self.physician_signature.path)[0] if self.has_physician_signature else ""

    @property
    def witness_signature_file_mime(self):
        return mimetypes.MimeTypes().guess_type(self.witness_signature.path)[0] if self.has_witness_signature else ""


