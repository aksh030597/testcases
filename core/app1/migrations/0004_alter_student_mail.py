# Generated by Django 4.1.5 on 2023-01-31 06:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_student_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mail',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
