from django import forms
from django.db import models
from django.forms import model_to_dict
from django.utils.text import slugify
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.search import index

from main.models.country import Country
from main.models.models import Thematic, Profile, ResourceType
from main.models.utils import (
    TimeStampedModel,
    SIMPLE_RICH_TEXT_FIELD_FEATURE,
    FreeBodyField,
)


class Resource(index.Indexed, TimeStampedModel, FreeBodyField):
    countries = models.ManyToManyField(Country, verbose_name="Pays", blank=True)
    name = models.CharField(verbose_name="Nom", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de la ressource)",
        unique=True,
        blank=True,
        default="",
        help_text="ce champ est rempli automatiquement s'il est laissé vide",
    )
    thematics = models.ManyToManyField(
        Thematic, blank=True, verbose_name="Thématiques", related_name="ressources"
    )
    main_thematic = models.ForeignKey(
        Thematic,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Thématique principale",
        help_text="ce champ n'est utilisé que lorsque plusieurs thématiques sont sélectionnées",
    )
    profiles = models.ManyToManyField(
        Profile, blank=True, verbose_name="Profiles", related_name="ressources"
    )
    geo_dev_creation = models.BooleanField(
        default=False, verbose_name="Créé par GeoDEV ?"
    )
    source_name = models.CharField(
        verbose_name="Nom de la source", max_length=100, blank=True
    )
    source_link = models.CharField(
        verbose_name="Lien de la source", max_length=100, blank=True
    )
    short_description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description courte",
    )
    types = models.ManyToManyField(ResourceType, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("short_description"),
        FieldPanel("body"),
        FieldPanel("types", widget=forms.CheckboxSelectMultiple),
        FieldPanel("thematics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("profiles", widget=forms.CheckboxSelectMultiple),
        FieldPanel("geo_dev_creation"),
        FieldPanel("source_name"),
        FieldPanel("source_link"),
        FieldPanel("countries", widget=forms.CheckboxSelectMultiple),
    ]

    def to_dict(self):
        to_return = model_to_dict(
            self,
            fields=[
                "name",
                "slug",
                "thematics",
                "profiles__name",
                "geo_dev_creation",
                "source_name",
                "short_description",
            ],
        )
        to_return["link"] = self.link
        to_return["profiles"] = [profile.slug for profile in self.profiles.all()]
        to_return["thematics"] = [thematic.slug for thematic in self.thematics.all()]
        if len(to_return["thematics"]) == 1:
            to_return["thematic"] = to_return["thematics"][0]
        elif len(to_return["thematics"]) > 1 and self.main_thematic:
            to_return["thematic"] = self.main_thematic.slug
        else:
            to_return["thematic"] = "multiple"
        zones = {country.zone.slug for country in self.countries.all()}
        if len(zones) == 1:
            to_return["zone"] = "south_africa"
        else:
            to_return["zone"] = None
        to_return["countries"] = [country.code for country in self.countries.all()]
        to_return["types"] = [type_.slug for type_ in self.types.all()]
        return to_return

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # if "GLOBAL" country is selected, select all countries
        for country in self.countries:
            if country.name == "GLOBAL":
                for country in Country.objects.all():
                    self.countries.add(country)
        super().save(*args, **kwargs)

    @property
    def link(self):
        from main.templatetags.main_tags import ressource_page_url

        return ressource_page_url(self)

    class Meta:
        verbose_name_plural = "Ressources"
        verbose_name = "Ressource"
        ordering = ["-created"]
