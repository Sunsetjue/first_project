# Generated by Django 2.0 on 2019-02-13 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20190212_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseteacher',
            name='profile',
            field=models.CharField(max_length=200),
        ),
    ]