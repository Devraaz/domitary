# Generated by Django 4.0.4 on 2022-05-20 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hostel_detail',
            old_name='type',
            new_name='hstl_type',
        ),
        migrations.AlterField(
            model_name='hostel_detail',
            name='phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='hostel_detail',
            name='zip',
            field=models.CharField(max_length=10),
        ),
    ]
