# Generated by Django 2.0 on 2019-02-08 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_news'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-timer']},
        ),
    ]
