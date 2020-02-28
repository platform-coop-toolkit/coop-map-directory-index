# Generated by Django 3.0.3 on 2020-02-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdi', '0023_tool_languages_supported'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='tool',
            name='languages_supported',
            field=models.ManyToManyField(to='mdi.Language'),
        ),
    ]
