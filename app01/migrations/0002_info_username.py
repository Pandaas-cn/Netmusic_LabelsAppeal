# Generated by Django 2.2 on 2020-04-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='username',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
