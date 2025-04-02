# Generated by Django 4.2.17 on 2025-03-19 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_delete_marktrack'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=255, verbose_name='IP Address')),
                ('port', models.IntegerField(verbose_name='Port')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('password', models.CharField(max_length=255, verbose_name='Password')),
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
                ('arrival', models.TimeField(null=True, verbose_name='Время прихода персоны')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.naturalperson')),
            ],
        ),
    ]
