# Generated by Django 4.0.4 on 2022-05-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0004_rename_hstl_name_hostel_detail_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel_detail',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
