# Generated by Django 3.1.3 on 2021-02-23 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0046_getintouch'),
    ]

    operations = [
        migrations.AddField(
            model_name='getintouch',
            name='sent',
            field=models.IntegerField(null=True),
        ),
    ]
