# Generated by Django 2.0 on 2019-02-09 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('image_url', models.URLField()),
                ('link_to', models.URLField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cms.News'),
        ),
    ]
