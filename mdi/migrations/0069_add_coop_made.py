# Generated by Django 3.0.3 on 2020-05-26 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0068_survey_to_models_manytomany'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='coop_made',
            field=models.CharField(choices=[('unknown', 'Not sure'), ('yes', 'Yes'), ('no', 'No')], default=0, max_length=16, verbose_name='Made by a cooperative'),
        ),
    ]
