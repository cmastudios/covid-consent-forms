# Generated by Django 3.0.4 on 2020-03-25 06:06

import consent.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0016_patientconsent_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientconsent',
            name='ability_to_consent',
            field=models.IntegerField(choices=[(2, 'No'), (1, 'Yes')], default=1),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='patient_signature',
            field=models.FileField(blank=True, null=True, upload_to=consent.models.get_patient_consent_file_path),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='physician_signature',
            field=models.FileField(blank=True, null=True, upload_to=consent.models.get_patient_consent_file_path),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='witness_signature',
            field=models.FileField(blank=True, null=True, upload_to=consent.models.get_patient_consent_file_path),
        ),
    ]