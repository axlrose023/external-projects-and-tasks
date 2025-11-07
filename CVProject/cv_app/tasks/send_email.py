from celery import shared_task
from cv_app.services.emails.service import EmailService


@shared_task
def send_cv_pdf_email(cv_pk: int, recipient: str):
    EmailService().send_cv_pdf(cv_pk, recipient)
