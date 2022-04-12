from typing import List

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

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
