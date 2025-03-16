# Generated by Django 4.2.17 on 2025-03-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0007_alter_department_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival', models.IntegerField(blank=True, null=True, verbose_name='Время прихода персоны')),
                ('leaving', models.IntegerField(blank=True, null=True, verbose_name='Время Ухода персоны')),
                ('is_late', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='workhours',
            name='arrival',
        ),
        migrations.RemoveField(
            model_name='workhours',
            name='leaving',
        ),
        migrations.AddField(
            model_name='workhours',
            name='arrive',
            field=models.IntegerField(blank=True, null=True, verbose_name='Время прихода'),
        ),
        migrations.AddField(
            model_name='workhours',
            name='leave',
            field=models.IntegerField(blank=True, null=True, verbose_name='Время Ухода'),
        ),
    ]
