# Generated by Django 3.0.3 on 2020-04-09 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_auto_20200407_0005'),
        ('mdi', '0059_auto_20200405_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='socialnetworks',
            field=models.ManyToManyField(blank=True, through='mdi.OrganizationSocialNetwork', to='accounts.SocialNetwork'),
        ),
        migrations.AlterField(
            model_name='organizationsocialnetwork',
            name='identifier',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organizationsocialnetwork',
            name='socialnetwork',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.SocialNetwork'),
        ),
    ]
