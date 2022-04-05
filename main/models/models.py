from typing import List

from django.db import models
from django.templatetags.static import static
from taggit.models import TagBase
from unidecode import unidecode
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtail.snippets.models import register_snippet

from main.models.utils import FreeBodyField, SIMPLE_RICH_TEXT_FIELD_FEATURE


class ContentPage(Page, FreeBodyField):
    class Meta:
        verbose_name = "Page de contenu"
        verbose_name_plural = "Pages de contenu"

    subpage_types: List[str] = []

    content_panels = Page.content_panels + FreeBodyField.panels


@register_snippet
class Profile(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        return static(f"img/{self.slug}.svg")

    @property
    def slug(self):
        return unidecode(self.name.lower())

    @property
    def ressources_link(self):
        from main.models.resources_page import ResourcesPage

        return f"{pageurl({}, ResourcesPage.objects.get())}?profile={self.slug}"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"


@register_snippet
class Thematic(TagBase):
    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"


@register_snippet
class ActualityType(TagBase):
    class Meta:
        verbose_name = "Type d'actualité"
        verbose_name_plural = "Types d'actualité"


@register_setting
class NewsLetterSettings(BaseSetting):
    newsLetter = models.URLField(
        help_text="Lien d'inscription à la lettre d'information",
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Inscription à la lettre d'information"
