# Generated by Django 5.0 on 2023-12-23 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_discount_carowner_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='carOwner_ID',
            new_name='carID',
        ),
    ]
