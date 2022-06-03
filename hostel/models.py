from random import choices
from django.db import models
import datetime, os
from django.contrib.auth.models import User

# Create your models here.

CITY= (
    ('Bhubaneswar','Bhubaneswar'),
    ('Cuttack', 'Cuttack')
)

GENDER = (
    ('Boys Hostel','Boys Hostel'),
    ('Girls Hostel','Girls Hostel')
)
GENDER_C = (
    ('Male','Male'),
    ('Female','Female')
)
POS = (
    ('1', '1 week'),
    ('2', '2 week'),
    ('3', '1 month'),
    ('4', '2 month'),
    ('5', '3 month'),
    ('6', '4 month'),
    ('7', '5 month'),
    ('8', '6 month'),
    
)

def get_filename(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/idproof', filename)
def get_image(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/', filename)

def get_prof(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/customer', filename)

def get_idprof(instance, filename):
    old_name = filename
    current_time = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(current_time, old_name)
    return os.path.join('media/customer', filename)


class Hostel_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    hstl_name= models.CharField(max_length = 100, default = 'Hostel')
    street = models.CharField(max_length=100)

    latitude = models.CharField(max_length=50, default = '0.0')
    longitude = models.CharField(max_length = 50, default = '0.0')
    city = models.CharField(choices = CITY, max_length=(30) )
    hstl_type = models.CharField(choices = GENDER, max_length=30)
    zip = models.CharField(max_length=10)
    
    rooms = models.IntegerField()
    beds = models.IntegerField()
    ppw = models.IntegerField()
    ppm = models.IntegerField()
    rooms_avail = models.IntegerField()
    aadhar = models.CharField(max_length = 12)
    id_proof = models.ImageField(upload_to=get_filename, null=True, blank = True)
    image  = models.ImageField(upload_to=get_image, null=True, blank = True)


    def __str__(self):
        return self.username
      


class Cust_details(models.Model):
    first_name =models.CharField(max_length = 50)
    last_name =models.CharField(max_length = 50)
    email =models.EmailField()
    username =models.CharField(max_length = 50)
    password =models.CharField(max_length = 128)
    
    phone =models.CharField(max_length = 10)
    gender =models.CharField(choices = GENDER_C, max_length = 20)
    dob =models.DateField(max_length = 50)
    
    address =models.CharField(max_length = 50)
    city =models.CharField(max_length = 50)
    pin_code =models.IntegerField()
    id_proof = models.ImageField(upload_to=get_filename, null=True, blank = True)
    profile_pic = models.ImageField(upload_to=get_prof, null=True, blank = True)


    def __str__(self):
        return self.first_name


class activity_log(models.Model):
    cust_name = models.CharField(max_length = 50)
    cust_email = models.CharField(max_length = 50)
    cust_phone = models.CharField(max_length = 50)
    check_in = models.DateField()
    pos = models.CharField(max_length = 30 )
    price =models.PositiveIntegerField()
    cust_id_proof = models.ImageField(upload_to=get_idprof, null=True, blank = True)

    bed = models.PositiveIntegerField()
    guest = models.PositiveIntegerField()

    owner_uname = models.CharField(max_length = 50)
    hstl_name = models.CharField(max_length = 50)
    date = models.DateField()

    def __str__(self) :
        return self.hstl_name
