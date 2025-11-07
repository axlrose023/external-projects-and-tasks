from django.views.generic import DetailView

from cv_app.models import CV
from cv_app.services.translation.supported_languages import SUPPORTED_LANGUAGES


class CVDetailView(DetailView):
    model = CV
    template_name = "cv_app/cv_detail.html"
    context_object_name = "cv"

    def get_queryset(self):
        return CV.objects.only(
            "id", "firstname", "lastname", "bio", "skills", "projects",
            "contacts"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["languages"] = SUPPORTED_LANGUAGES
        ctx["translated"] = self.request.session.pop("translated", None)
        return ctx
