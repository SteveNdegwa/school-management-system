# Generated by Django 5.0.4 on 2024-12-22 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identities', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='identity',
            options={'ordering': ('-date_created',), 'verbose_name_plural': 'Identities'},
        ),
    ]