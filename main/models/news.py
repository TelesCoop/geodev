import datetime

from django import forms
from django.db import models
from django.forms import model_to_dict
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from main.models.models import ActualityType
from main.models.utils import TimeStampedModel
from main.templatetags.main_tags import news_page_url


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

    def link(self):
        return news_page_url(self)

    def to_dict(self):
        to_return = model_to_dict(
            self,
            fields=[
                "name",
                "publication_date",
                "slug",
            ],
        )
        to_return["publication_date"] = self.publication_date.isoformat()
        to_return["types"] = [type_.slug for type_ in self.types.all()]
        # to_return["image_link"] = self.image.url

        return to_return

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-publication_date"]
