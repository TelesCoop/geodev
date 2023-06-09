import datetime

from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.views.serve import generate_image_url
from wagtail.search import index

from main.models.country import Country, WorldZone
from main.models.models import ActualityType
from main.models.models import Thematic
from main.models.resource import Resource
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
        verbose_name="Miniature",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_geodev = models.BooleanField(
        verbose_name="Est une nouvelle GeoDEV",
        help_text="La première actualité mise en avant sur la page d'accueil est la dernière actualité GeoDEV",
        default=False,
    )
    types = models.ManyToManyField(
        ActualityType,
        blank=True,
        verbose_name="Type",
        related_name="news",
        help_text="Permet le filtrage des actualités",
    )
    is_global = models.BooleanField(
        verbose_name="Concerne tous les pays", default=False
    )
    countries = models.ManyToManyField(
        Country,
        verbose_name="Pays liés",
        blank=True,
        help_text="Ce champ n'est pas encore utilisé",
    )
    zones = models.ManyToManyField(
        WorldZone,
        blank=True,
        verbose_name="Zones du monde liées",
        help_text="Ce champ n'est pas encore utilisé",
    )
    thematics = models.ManyToManyField(
        Thematic,
        blank=True,
        verbose_name="Thématiques liées",
        help_text="Ce champ n'est pas encore utilisé",
    )
    resources = models.ManyToManyField(
        Resource, blank=True, verbose_name="Ressources liées"
    )

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.FilterField("publication_date"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("slug", classname="full"),
        FieldPanel("publication_date"),
        FieldPanel("image"),
        FieldPanel("introduction"),
        FieldPanel("is_geodev"),
        FieldPanel("body"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("is_global"),
        FieldPanel("zones", widget=forms.CheckboxSelectMultiple),
        FieldPanel("countries", widget=forms.SelectMultiple),
        FieldPanel("thematics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("resources", widget=forms.SelectMultiple),
    ]

    def __str__(self):
        return self.name

    @property
    def link(self):
        return news_page_url(news=self)

    def to_dict(self, include_linked=True):
        to_return = model_to_dict(
            self,
            fields=[
                "id",
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

        if include_linked:
            # without this check, there could be an infinite loop in linked news
            to_return["resources"] = [
                resource.to_dict() for resource in self.resources.all()
            ]

        return to_return

    def add_countries_from_zone(self):
        # add all countries of all selected zones
        for zone in self.zones.all():
            for country in zone.country_set.all():
                self.countries.add(country)
        super().save()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-publication_date"]
