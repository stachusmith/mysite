# Generated by Django 3.1.3 on 2020-12-02 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_view', '0013_auto_20201201_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='picture',
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.BinaryField(blank=True, editable=True, null=True)),
                ('content_type', models.CharField(blank=True, help_text='The MIMEType of the file', max_length=256, null=True)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_view.topic')),
            ],
        ),
    ]
