# Generated by Django 5.2.3 on 2025-06-26 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0005_alter_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="outfititem",
            name="brand",
            field=models.CharField(default="brand", max_length=100),
            preserve_default=False,
        ),
    ]
