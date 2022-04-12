import datetime

from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.views.serve import generate_image_url
from wagtail.search import index

from main.models.models import ActualityType
from main.models.utils import TimeStampedModel, FreeBodyField
from main.templatetags.main_tags import news_page_url


class News(index.Indexed, TimeStampedModel, FreeBodyField):
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
        blank=True,
        default="",
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )
    introduction = RichTextField(max_length=250)
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
        FieldPanel("introduction"),
        FieldPanel("body"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.name

    @property
    def link(self):
        return news_page_url(news=self)

    def to_dict(self):
        to_return = model_to_dict(
            self,
            fields=[
                "name",
                "publication_date",
                "slug",
            ],
        )
        to_return["publication_date"] = self.publication_date.strftime("%d %B %Y")
        to_return["types"] = [type_.slug for type_ in self.types.all()]
        if self.image:
            to_return["image_link"] = generate_image_url(self.image, "fill-432x220")
        else:
            to_return["image_link"] = None
        to_return["introduction"] = str(self.introduction)
        to_return["link"] = self.link

        return to_return

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-publication_date"]
