# Generated by Django 3.1.3 on 2021-01-29 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0037_auto_20210129_2034'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together={('project', 'participant')},
        ),
    ]
