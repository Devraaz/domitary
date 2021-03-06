# Generated by Django 4.0.4 on 2022-05-24 05:22

from django.db import migrations, models
import hostel.models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0007_remove_hostel_detail_locality_hostel_detail_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cust_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20)),
                ('dob', models.DateField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('pin_code', models.IntegerField()),
                ('id_proof', models.ImageField(blank=True, null=True, upload_to=hostel.models.get_filename)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=hostel.models.get_prof)),
            ],
        ),
    ]
