# Generated by Django 3.1.3 on 2021-02-23 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0047_getintouch_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='getintouch',
            name='name',
            field=models.CharField(default=0, max_length=200, validators=[django.core.validators.MinLengthValidator(1, 'Title must be greater than 1 character')]),
            preserve_default=False,
        ),
    ]
