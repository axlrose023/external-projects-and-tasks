from django.urls import path

from .views import *

urlpatterns = [
    path('create_user_site/', create_user_site, name='create_user_site'),
    path('delete_site/<int:site_id>/', delete_user_site, name='delete_user_site'),
]
