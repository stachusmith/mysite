# Generated by Django 3.1.3 on 2020-11-30 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_view', '0010_topic_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='topic_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='topic_title',
            new_name='title',
        ),
    ]
