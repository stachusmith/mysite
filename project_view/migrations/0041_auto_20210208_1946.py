# Generated by Django 3.1.3 on 2021-02-08 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0040_auto_20210208_1418'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together=set(),
        ),
    ]