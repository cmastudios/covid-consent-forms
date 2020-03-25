import mimetypes

from django.db import models

class SignatureField(models.FileField):

    def __init__(self, file_name):
        super(SignatureField, self).__init__(*args, **kwargs)

    def clean(self):
        if False:
            raise forms.ValidationError("Filetype not allowed! Please upload a video or hand draw the signature.")