# Generated by Django 3.2.11 on 2022-04-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_auto_20220404_1206"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="resource_type",
            field=models.CharField(
                choices=[
                    ("data", "Donnée"),
                    ("training", "Support de formation"),
                    ("product", "Produit thématique"),
                ],
                default="data",
                max_length=20,
            ),
        ),
    ]
