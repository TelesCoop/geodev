from typing import List

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from main.forms import ContactForm
from main.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE


class ContactPage(Page):
    class Meta:
        verbose_name = "Page de contact"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    left_column = RichTextField(
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE + ["h2", "h3", "h4", "ol", "ul"],
        verbose_name="colonne de gauche",
    )
    newsletter_text = RichTextField(
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="texte d'introduction newsletter",
    )

    content_panels = Page.content_panels + [
        FieldPanel("left_column"),
        FieldPanel("newsletter_text"),
    ]

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                send_mail(
                    subject=f"[Geodev] {form.cleaned_data['subject']}",
                    message=form.cleaned_data["message"],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=settings.CONTACT_RECIPIENTS,
                )
                return render(
                    request,
                    "main/contact_page.html",
                    {"validated": True},
                )
        else:
            form = ContactForm()

        context = self.get_context(request)
        context["form"] = form
        context["review_selected"] = bool(request.GET.get("review"))
        return render(
            request,
            "main/contact_page.html",
            context,
        )
