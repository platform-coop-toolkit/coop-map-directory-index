# Generated by Django 3.0.3 on 2020-05-28 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0069_add_coop_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='license_type',
            field=models.CharField(blank=True, choices=[('proprietary', 'Proprietary'), ('proprietary-with-floss-integration-tools', 'Proprietary with free / libre / open source integration tools'), ('floss', 'Free / libre / open source')], default='', max_length=64, verbose_name='License type'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mdi.License', verbose_name='Free / libre / open source license'),
        ),
    ]
