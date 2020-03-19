# Generated by Django 3.0.4 on 2020-03-19 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0005_patientconsent_relative_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientconsent',
            name='nurse_signature',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patientconsent',
            name='physician_signature',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='consent_video',
            field=models.FileField(upload_to='videos/'),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='inability',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='relative_name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
