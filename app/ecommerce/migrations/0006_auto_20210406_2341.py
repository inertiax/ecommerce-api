# Generated by Django 3.1.4 on 2021-04-06 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ecommerce", "0005_auto_20210405_2136"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="ecommerce.product",
            ),
        ),
    ]
