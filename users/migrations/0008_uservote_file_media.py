# Generated by Django 4.0.10 on 2023-03-24 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_uservote_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservote',
            name='file_media',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]