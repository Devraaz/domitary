from django.contrib import admin

from hostel.models import Cust_details, activity_log, Hostel_detail

# Register your models here.
admin.site.register(Hostel_detail)
admin.site.register(Cust_details)
admin.site.register(activity_log)