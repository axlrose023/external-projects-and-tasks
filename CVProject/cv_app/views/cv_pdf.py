from django.http import Http404, HttpResponse
from django.views import View

from cv_app.models import CV
from cv_app.services.pdf import CVPdfService


class CVPdfView(View):
    def get(self, request, pk: int):
        service = CVPdfService()
        try:
            pdf = service.build_for_pk(pk)
        except CV.DoesNotExist:
            raise Http404()

        resp = HttpResponse(pdf, content_type="application/pdf")
        resp["Content-Disposition"] = f'attachment; filename="cv-{pk}.pdf"'
        return resp