from django.urls import path
from .views import (
    SpyCatList,
    SpyCatDetail,
    MissionList,
    MissionDetail,
    MissionAssignCat,
    MissionComplete,
    TargetList,
    TargetDetail,
    TargetComplete,
)

urlpatterns = [

    path('spycats/', SpyCatList.as_view(), name='spycat-list'),
    path('spycats/<int:pk>/', SpyCatDetail.as_view(), name='spycat-detail'),

    path('missions/', MissionList.as_view(), name='mission-list'),
    path('missions/<int:pk>/', MissionDetail.as_view(), name='mission-detail'),
    path('missions/<int:pk>/assign_cat/', MissionAssignCat.as_view(), name='mission-assign-cat'),
    path('missions/<int:pk>/complete/', MissionComplete.as_view(), name='mission-complete'),

    path('targets/', TargetList.as_view(), name='target-list'),
    path('targets/<int:pk>/', TargetDetail.as_view(), name='target-detail'),
    path('targets/<int:pk>/complete/', TargetComplete.as_view(), name='target-complete'),
]
