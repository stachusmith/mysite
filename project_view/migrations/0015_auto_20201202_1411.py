# Generated by Django 3.1.3 on 2020-12-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0014_auto_20201202_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
