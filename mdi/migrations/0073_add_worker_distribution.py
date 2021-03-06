# Generated by Django 3.0.3 on 2020-06-01 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0072_add_org_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='worker_distribution',
            field=models.CharField(blank=True, choices=[('colocated', 'Co-located'), ('regional', 'Regionally distributed'), ('national', 'Nationally distributed'), ('international', 'Internationally distributed')], default='', max_length=64),
        ),
    ]
