from django.contrib import admin
from . import models

admin.site.register(models.PatientConsent)
admin.site.register(models.Operation)


