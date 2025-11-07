from django.urls import path
from .views import CVListView, CVDetailView, CVPdfView, SettingsView, \
    SendCvEmailView
from .views.translave_cv_view import TranslateCvView

urlpatterns = [
    path("", CVListView.as_view(), name="cv_list"),
    path("cv/<int:pk>/", CVDetailView.as_view(), name="cv_detail"),
    path("cv/<int:pk>/pdf/", CVPdfView.as_view(), name="cv_pdf"),
    path(
        "cv/<int:pk>/email/send/", SendCvEmailView.as_view(),
        name="cv_send_email"
    ),
    path(
        "cv/<int:pk>/translate/", TranslateCvView.as_view(), name="cv_translate"
        ),

    path("settings/", SettingsView.as_view(), name="settings_page"),

]
