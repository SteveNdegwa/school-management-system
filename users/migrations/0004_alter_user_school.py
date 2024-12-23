# Generated by Django 5.0.4 on 2024-12-22 13:48

import base.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('users', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.ForeignKey(default=base.models.School.default, on_delete=django.db.models.deletion.CASCADE, to='base.school'),
        ),
    ]