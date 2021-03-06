# Generated by Django 2.2 on 2020-04-21 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('musiclink', models.CharField(blank=True, max_length=50)),
                ('system_label', models.CharField(blank=True, max_length=10)),
                ('user_label', models.CharField(blank=True, max_length=10)),
                ('userid', models.CharField(blank=True, max_length=20)),
                ('imgfile', models.CharField(blank=True, max_length=50)),
                ('checklabel', models.CharField(blank=True, max_length=5)),
                ('status', models.CharField(default='申诉提交', max_length=5)),
                ('submit_time', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
