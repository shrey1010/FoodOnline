# Generated by Django 4.2.3 on 2023-09-03 06:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vendor", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vendor",
            old_name="User",
            new_name="user",
        ),
    ]