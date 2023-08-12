from django.urls import path
from .views import * 

import django

app_name = 'core'

urlpatterns = [
    path('',index, name='index'),
]


django.setup()