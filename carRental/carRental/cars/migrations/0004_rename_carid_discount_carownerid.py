# Generated by Django 5.0 on 2023-12-23 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_rename_carowner_id_discount_carid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='carID',
            new_name='carOwnerID',
        ),
    ]
