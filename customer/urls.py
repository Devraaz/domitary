from django.urls import path
from hostel import views

urlpatterns = [
    path('python{{', views.index, name='home' ),
]