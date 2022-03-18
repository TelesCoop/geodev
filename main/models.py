import json
import datetime
from typing import List

from django.db import models
from django import forms
from django.http import Http404
from taggit.models import TagBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from main.countries import COUNTRIES

from wagtail.core.models import Page

SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link"]


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class HomePage(Page):
    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction du block des ressources",
    )
    ressources_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du block des ressources",
        max_length=64,
        default="Des ressources adaptées à votre profil",
    )
    ressources_block_introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction du block des ressources",
    )
    ressources_block_explication = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Explication du block des ressources",
        help_text="Explication présente sous les listes des différents profils",
    )
    news_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du block des actualités",
        max_length=64,
        default="Dernières actualités",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("ressources_block_title"),
        FieldPanel("ressources_block_introduction"),
        FieldPanel("ressources_block_explication"),
        FieldPanel("news_block_title"),
    ]

    class Meta:
        verbose_name = "Page d'accueil"


class RessourcesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des ressources"
        verbose_name_plural = "Pages des ressources"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="ressource")
    def access_ressource_page(self, request, news_slug):
        try:
            ressource = Ressource.objects.get(slug=news_slug, locale_id=self.locale_id)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404
        return self.render(
            request,
            context_overrides={
                "ressource": ressource,
                # There is only one RessourcesPage if there is only one language
                "ressource_page": RessourcesPage.objects.first(),
            },
            template="main/ressource_page.html",
        )


class NewsListPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des actualités"
        verbose_name_plural = "Pages des actualités"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="news")
    def access_news_page(self, request, news_slug):
        try:
            news = News.objects.get(slug=news_slug, locale_id=self.locale_id)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404
        return self.render(
            request,
            context_overrides={
                "news": news,
                # There is only one NewsListPage if there is only one language
                "news_page": NewsListPage.objects.first(),
            },
            template="main/news_page.html",
        )


class Map(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["ressources_per_country"] = json.dumps(
            {
                "CM": [
                    {
                        "name": "My Element",
                    }
                ]
            }
        )
        context["country_parameters"] = json.dumps(
            {"CM": {"lng": 13.6299563, "lat": 4.814121, "name": "Cameroun"}}
        )
        return context


@register_snippet
class Profile(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Description",
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profiles",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
        ImageChooserPanel("icon"),
    ]

    def __str__(self):
        return self.name

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


@register_snippet
class Ressource(index.Indexed, TimeStampedModel):
    country = models.CharField(max_length=50, choices=COUNTRIES, verbose_name="Pays")
    name = models.CharField(verbose_name="Nom", max_length=100)
    slug = models.SlugField(
        max_length=100,
        verbose_name="Slug (URL de la ressource)",
        unique=True,
        default="",
    )
    thematics = models.ManyToManyField(
        Thematic, blank=True, verbose_name="Thématiques", related_name="ressources"
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
        help_text="Sera affiché sur la carte de la ressource",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("country"),
        FieldPanel("thematics", widget=forms.CheckboxSelectMultiple),
        FieldPanel("profiles", widget=forms.CheckboxSelectMultiple),
        FieldPanel("geo_dev_creation"),
        FieldPanel("source_name"),
        FieldPanel("source_link"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ressources"
        verbose_name = "Ressource"
        ordering = ["-created"]


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
