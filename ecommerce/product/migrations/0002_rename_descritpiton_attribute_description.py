# Generated by Django 4.2 on 2023-04-24 18:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="attribute",
            old_name="descritpiton",
            new_name="description",
        ),
    ]
