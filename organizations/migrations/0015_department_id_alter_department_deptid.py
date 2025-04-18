# Generated by Django 4.2.17 on 2025-03-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0014_rename_departmenttitle_department_deptname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='deptID',
            field=models.IntegerField(unique=True, verbose_name='ID'),
        ),
    ]
