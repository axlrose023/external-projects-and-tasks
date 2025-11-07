from django.urls import path

from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('change-password/', change_password, name='change_password'),
    path('logout/', user_logout, name='user_logout'),
]
