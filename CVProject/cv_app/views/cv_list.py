from django.views.generic import ListView

from cv_app.models import CV


class CVListView(ListView):
    model = CV
    template_name = "cv_app/cv_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            CV.objects.only("id", "firstname", "lastname", "bio", "skills")
            .order_by("lastname", "firstname")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["total"] = self.object_list.count()
        return ctx