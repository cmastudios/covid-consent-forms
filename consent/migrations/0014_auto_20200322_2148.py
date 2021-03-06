# Generated by Django 3.0.4 on 2020-03-23 02:48

import consent.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0013_auto_20200322_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='consent_form',
            field=models.FileField(upload_to=consent.models.get_form_type_file_path),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='ability_to_consent',
            field=models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='attending_physician',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name of attending physician'),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='consenting_physician',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name of physician obtaining consent'),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='patient_dob',
            field=models.DateField(verbose_name='Patient Date of Birth'),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='patient_mrn',
            field=models.CharField(max_length=64, verbose_name='Patient MRN'),
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
            name='witness_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name of witness'),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='witness_signature',
            field=models.FileField(blank=True, null=True, upload_to=consent.models.get_patient_consent_file_path),
        ),
    ]
