# Generated by Django 4.0.10 on 2023-03-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='page',
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=models.ManyToManyField(related_name='user_option', to='questions.option'),
        ),
    ]
