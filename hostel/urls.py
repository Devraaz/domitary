from django.contrib import admin
from django.urls import path,include
from hostel import views

from django.conf.urls.static import static
from django.conf import settings
from hostel import views

urlpatterns = [
    path('', views.index, name='home' ),
    path('about', views.about, name='about' ),
    path('register', views.register, name='register' ),
    path('cust_register', views.cust_register, name='cust_register'),
    path('login', views.login, name='login' ),

    path('cust_logout', views.cust_logout, name='cust_logout'),
    path('cust_login', views.cust_login, name='cust_login'),
    path('cust_profile', views.cust_profile, name='cust_profile'),
    path('cust_booking', views.cust_booking, name='cust_booking'),
    path('booking', views.booking, name='booking'),
    path('confirm', views.confirm, name='confirm'),
    

    
    path('details/dashboard' , views.dashboard, name='dashboard'),
    path("details/logout", views.logout, name='logout'),
    path('details/prof_detail', views.prof_detail, name='prof_detail'),
    path('details/hstl_activity', views.hstl_activity, name='hstl_activity'),
    path('details/std_detail', views.std_detail, name='std_detail'),
    path('details/hstl_details', views.hstl_details, name='hstl_details'),
    path('details/update_hstl', views.update_hstl, name='update_hstl'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
