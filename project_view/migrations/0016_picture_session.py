# Generated by Django 3.1.3 on 2020-12-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0015_auto_20201202_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='session',
            field=models.IntegerField(null=True),
        ),
    ]
