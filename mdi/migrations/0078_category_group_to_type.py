# Generated by Django 3.0.3 on 2020-06-17 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0077_add_category_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_group',
        ),
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mdi.Type'),
        ),
    ]
