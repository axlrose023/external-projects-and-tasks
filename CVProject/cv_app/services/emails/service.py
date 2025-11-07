
from __future__ import annotations
from django.core.mail import EmailMessage
from cv_app.models import CV
from cv_app.services.pdf.service import CVPdfService


class EmailService:


    def __init__(self, pdf_service: CVPdfService | None = None) -> None:
        self.pdf_service = pdf_service or CVPdfService()

    def send_cv_pdf(self, cv_pk: int, recipient: str) -> None:
        cv = CV.objects.only("firstname", "lastname").get(pk=cv_pk)

        pdf_bytes = self.pdf_service.build_for_pk(cv_pk)

        subject = f"CV — {cv.firstname} {cv.lastname}"
        body = "Please find attached the requested CV."
        email = EmailMessage(subject, body, to=[recipient])

        filename = f"cv-{cv_pk}.pdf"
        email.attach(filename, pdf_bytes, "application/pdf")

        email.send()
