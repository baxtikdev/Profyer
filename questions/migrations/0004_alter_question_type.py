# Generated by Django 4.0.10 on 2023-03-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('CHOICE', 'CHOICE'), ('CHECKBOX', 'CHECKBOX'), ('NUMBER', 'NUMBER'), ('AGE', 'AGE'), ('COUNTRY', 'COUNTRY')], default='CHOICE', max_length=10),
        ),
    ]
