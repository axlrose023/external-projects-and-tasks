from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages

from cv_app.models import CV
from cv_app.services.translation.service import TranslationService
from cv_app.services.translation.supported_languages import SUPPORTED_LANGUAGES

class TranslateCvView(View):

    def post(self, request, pk, *args, **kwargs):
        cv = get_object_or_404(CV.objects.only("id"), pk=pk)

        lang = request.POST.get("language", "")
        if lang not in SUPPORTED_LANGUAGES:
            messages.error(request, "Unsupported language.")
            return redirect("cv_detail", pk=pk)

        try:
            svc = TranslationService()
            translated = svc.translate(pk, lang)
        except Exception as e:
            messages.error(request, f"Translation failed: {e}")
            return redirect("cv_detail", pk=pk)

        context = {
            "cv": cv,
            "languages": SUPPORTED_LANGUAGES,
            "translated": translated,
        }
        return render(request, "cv_app/cv_detail.html", context)
