# Generated by Django 2.0 on 2019-02-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20190213_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseteacher',
            name='profile',
            field=models.CharField(max_length=1000),
        ),
    ]
