# Generated by Django 5.0 on 2023-12-23 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='carOwner_ID',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cars.carowner'),
            preserve_default=False,
        ),
    ]