# Generated by Django 4.2.4 on 2023-08-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_populate_tables_with_defaults"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweet",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="tweets", related_query_name="tweet", to="core.tag"),
        ),
    ]
