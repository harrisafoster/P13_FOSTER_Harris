# Generated by Django 3.0 on 2022-03-09 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0004_auto_20220309_1418'),
        ('profiles', '0002_auto_20220309_1423')
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
