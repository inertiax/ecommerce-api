# Generated by Django 3.1.4 on 2021-04-02 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="shipping",
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
        ),
    ]