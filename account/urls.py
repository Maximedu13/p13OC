""" account app urls """
from django.urls import path
from . import views # import views so we can use them in urls.

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
]