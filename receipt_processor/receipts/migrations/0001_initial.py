# Generated by Django 5.1.3 on 2024-11-19 07:55

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('retailer', models.CharField(max_length=255)),
                ('purchase_date', models.DateField()),
                ('purchase_time', models.TimeField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='receipts.receipt')),
            ],
        ),
    ]
