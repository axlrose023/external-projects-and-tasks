
from django.urls import path
from office import views

urlpatterns = [
    path('polar/<str:room_number>/', views.office_detail, name='office_detail'),
]
