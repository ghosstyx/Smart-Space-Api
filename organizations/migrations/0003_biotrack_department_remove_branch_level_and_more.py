# Generated by Django 4.2.17 on 2025-03-05 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_parent'),
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
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentTitle', models.CharField(max_length=255, verbose_name='Название Подразделения')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
        migrations.RemoveField(
            model_name='branch',
            name='level',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='tree_id',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='level',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='jobtitle',
            name='tree_id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='level',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='branch',
            name='branchTitle',
            field=models.CharField(max_length=255, verbose_name='Название филиала'),
        ),
    ]
