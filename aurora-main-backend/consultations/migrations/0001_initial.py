# Generated by Django 5.1.1 on 2025-04-08 18:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analysis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('REQUESTED', 'Requested'), ('SCHEDULED', 'Scheduled'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='REQUESTED', max_length=10)),
                ('scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.skinanalysis')),
                ('dermatologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_consultations', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-scheduled_time'],
                'permissions': [('can_manage_consultation', 'Can manage all consultations')],
            },
        ),
    ]
