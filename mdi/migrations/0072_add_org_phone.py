# Generated by Django 3.0.3 on 2020-05-28 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0071_add_org_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
