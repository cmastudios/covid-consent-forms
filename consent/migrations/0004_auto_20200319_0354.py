# Generated by Django 3.0.4 on 2020-03-19 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consent', '0003_auto_20200319_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientconsent',
            name='consent_status',
            field=models.IntegerField(choices=[(1, 'Consent given by patient'), (2, 'Consent given by guardian/relative (see relationship)'), (3, 'Inability to give consent (see reason)')], default=1),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='inability',
            field=models.CharField(default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='physician',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='physician', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='patientconsent',
            name='today_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
