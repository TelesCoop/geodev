import datetime

from django import forms
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from main.models.models import ActualityType
from main.models.utils import TimeStampedModel


@register_snippet
class News(index.Indexed, TimeStampedModel):
    name = models.CharField(verbose_name="nom", max_length=255)
    publication_date = models.DateTimeField(
        verbose_name="Date de publication",
        default=datetime.datetime.now,
        help_text="Permet de trier l'ordre d'affichage dans la page des actualités",
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de l'actualité)",
        unique=True,
        default="",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    types = models.ManyToManyField(
        ActualityType,
        blank=True,
        verbose_name="Type",
        related_name="news",
        help_text="Permet le filtrage des actualités",
    )

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("publication_date"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug", classname="full"),
        FieldPanel("publication_date"),
        ImageChooserPanel("image"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Actualités / Evènements"
        verbose_name = "Actualité / Evènement"
        ordering = ["-publication_date"]
