from turtle import home

from django.urls import path

from olt.views import home_olt

urlpatterns = [
    path('', home_olt, name='home_olt'),
]
