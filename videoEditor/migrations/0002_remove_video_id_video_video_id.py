# Generated by Django 4.2.7 on 2023-11-24 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoEditor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='id',
        ),
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
    ]
