# Generated by Django 3.0.3 on 2020-02-28 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0024_auto_20200228_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='pricing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mdi.Pricing'),
        ),
    ]