# Generated by Django 3.2.9 on 2021-12-04 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_auto_20211204_0626"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transfer",
            old_name="is_active",
            new_name="is_sold",
        ),
    ]
