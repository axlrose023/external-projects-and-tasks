from django.urls import path, include

urlpatterns = [
    path("v1/", include(("cv_api.v1.urls", "cv_api"), namespace="v1")),
]
