from django.shortcuts import redirect
from django.views import View
from django.contrib import messages

from cv_app.models import CV
from cv_app.tasks.send_email import send_cv_pdf_email

class SendCvEmailView(View):
    def post(self, request, pk, *args, **kwargs):
        CV.objects.only("id").get(pk=pk)

        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Please provide a valid email address.")
            return redirect("cv_detail", pk=pk)

        send_cv_pdf_email.delay(pk, email)
        messages.success(request, "Your request has been queued — you will receive the PDF shortly.")
        return redirect("cv_detail", pk=pk)