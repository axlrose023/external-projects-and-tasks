from django.views.generic import TemplateView

class SettingsView(TemplateView):
    template_name = "cv_app/settings.html"