# Generated by Django 5.2 on 2025-05-12 15:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BioTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=255, verbose_name='IP Address')),
                ('port', models.IntegerField(verbose_name='Port')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('password', models.CharField(default=1, max_length=255, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'Био Трек',
                'verbose_name_plural': 'Био Треки',
            },
        ),
        migrations.CreateModel(
            name='MarkTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkTime', models.DateTimeField(null=True, verbose_name='Время прихода персоны')),
                ('checkType', models.CharField(max_length=255, verbose_name='IN or OUT')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
