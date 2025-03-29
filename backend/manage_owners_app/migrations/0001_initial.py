# Generated by Django 5.1.7 on 2025-03-29 17:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='First name of the client.', max_length=200)),
                ('last_name', models.CharField(help_text='Last name of the client.', max_length=200)),
                ('email', models.EmailField(help_text="Client's primary email address.", max_length=254, unique=True)),
                ('phone_number', models.CharField(help_text="Client's primary phone number.", max_length=20)),
                ('address', models.TextField(blank=True, help_text="Client's physical address (optional).")),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Date the client was added to the system.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this client is currently active.')),
                ('notes', models.TextField(blank=True, help_text='General notes about the client (optional).')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['last_name'],
            },
        ),
    ]
