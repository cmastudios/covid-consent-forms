# Generated by Django 3.0.4 on 2020-03-26 05:39

import consent.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0018_auto_20200326_0033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientconsent',
            name='uuid',
        ),
        migrations.AddField(
            model_name='patientconsent',
            name='identifier',
            field=models.CharField(default=consent.models.generate_form_id, max_length=10),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='ability_to_consent',
            field=models.IntegerField(choices=[(2, 'No'), (1, 'Yes')], default=1),
        ),
    ]
