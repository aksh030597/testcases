# Generated by Django 4.1.5 on 2023-03-21 09:26

import app1.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_student_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mail',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(), app1.models.custom_validator]),
        ),
    ]