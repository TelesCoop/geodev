import json
import datetime
from typing import List

from django.db import models
from django import forms
from django.http import Http404
from django.templatetags.static import static
from taggit.models import TagBase
from unidecode import unidecode
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from main.constants import THEMATICS, ZONES
from main.countries import COUNTRIES

from wagtail.core.models import Page

SIMPLE_RICH_TEXT_FIELD_FEATURE = ["bold", "italic", "link"]
COLOR_CHOICES = (
    ("blue", "Bleue"),
    ("pink", "Rose"),
    ("white", "Blanche"),
    ("none", "Sans couleur"),
)


def paragraph_block(additional_field, required):
    return (
        "paragraph",
        blocks.RichTextBlock(
            label="Contenu",
            features=SIMPLE_RICH_TEXT_FIELD_FEATURE
            + ["h3", "h4", "ol", "ul"]
            + additional_field,
            required=required,
        ),
    )


class FreeBodyField(models.Model):
    color_block = (
        "color",
        blocks.ChoiceBlock(
            choices=COLOR_CHOICES,
            default="none",
            help_text="Couleur de fond",
        ),
    )

    body = StreamField(
        [
            # Is h1
            (
                "heading",
                blocks.CharBlock(form_classname="full title", label="Titre de la page"),
            ),
            (
                "section",
                blocks.StructBlock(
                    [
                        color_block,
                        (
                            "image",
                            ImageChooserBlock(
                                label="Image à côté du paragraphe", required=False
                            ),
                        ),
                        (
                            "position",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("right", "Droite"),
                                    ("left", "Gauche"),
                                ],
                                required=False,
                                help_text="Position de l'image",
                            ),
                        ),
                        paragraph_block(["h2"], True),
                        (
                            "sub_section",
                            blocks.ListBlock(
                                blocks.StructBlock(
                                    [
                                        color_block,
                                        paragraph_block([], False),
                                        (
                                            "columns",
                                            blocks.ListBlock(
                                                blocks.StructBlock(
                                                    [
                                                        color_block,
                                                        paragraph_block([], False),
                                                    ],
                                                    label="Colonne",
                                                ),
                                                label="Colonnes",
                                            ),
                                        ),
                                    ],
                                    label="Sous section",
                                ),
                                label="Sous sections",
                            ),
                        ),
                    ],
                    label="Section",
                ),
            ),
            ("image", ImageChooserBlock()),
            ("pdf", DocumentChooserBlock()),
        ],
        blank=True,
        verbose_name="Description",
        help_text="Corps de la page",
    )

    panels = [
        StreamFieldPanel("body", classname="full"),
    ]

    class Meta:
        abstract = True


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
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["n_ressources"] = 148
        context["n_members"] = 80
        context["profiles"] = Profile.objects.all()
        # context["profiles"] = [
        #     {
        #         "name": "décideurs",
        #         "description": """Élu local ou gestionnaire de territoire, accédez aux
        #             produits, services et tableaux de bord, documents
        #             de synthèse pour
        #             <span class="has-text-weight-bold">aider vos prises de décision</span>.""",
        #         "link": "/ressources",
        #         "link_text": "Voir les ressources",
        #     },
        #     {
        #         "name": "géomaticiens",
        #         "description": """Cartographe ou gestionnaire de bases de données géographiques,
        #                 accédez aux produits, applications et documents techniques pour
        #             <span class="has-text-weight-bold">faciliter et enrichir vos travaux</span>.""",
        #         "link": "/ressources",
        #         "link_text": "Voir les ressources",
        #     },
        #     {
        #         "name": "Télédétecteurs",
        #         "description": """Vous traitez des images satellitaires pour proposer
        #                 des services et vos projets de recherche,
        #                 <span class="has-text-weight-bold">
        #                     accédez plus facilement aux images disponibles, outils de traitement,
        #                     formations et ressources bibliographiques
        #                 </span>.""",
        #         "link": "/ressources",
        #         "link_text": "Voir les ressources",
        #     },
        # ]
        context["news_list"] = News.objects.all()[:3]
        # [
        #     {
        #         "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
        #         "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
        #         "date": "06.03.2022",
        #         "link": "/news/1",
        #         "image": "/static/img/home-intro-image.svg",
        #     },
        #     {
        #         "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
        #         "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
        #         "date": "06.03.2022",
        #         "link": "/news/1",
        #         "image": "/static/img/home-intro-image.svg",
        #     },
        #     {
        #         "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
        #         "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
        #         "date": "06.03.2022",
        #         "link": "/news/1",
        #         "image": "/static/img/home-intro-image.svg",
        #     },
        # ]
        context["newsletter_link"] = "newsletter-link"
        return context

    # HomePage can be created only on the root
    parent_page_types = ["wagtailcore.Page"]

    introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction",
    )
    ressources_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du bloc des ressources",
        max_length=64,
        default="Des ressources adaptées à votre profil",
    )
    ressources_block_introduction = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Introduction du bloc des ressources",
    )
    ressources_block_explication = RichTextField(
        null=True,
        blank=True,
        features=SIMPLE_RICH_TEXT_FIELD_FEATURE,
        verbose_name="Explication du bloc des ressources",
        help_text="Explication présente sous les listes des différents profils",
    )
    news_block_title = models.CharField(
        blank=True,
        verbose_name="Titre du bloc des actualités",
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["has_vue"] = True
        context["profiles"] = json.dumps(
            {
                profile.slug: {"name": profile.name, "slug": profile.slug}
                for profile in Profile.objects.all()
            }
        )
        context["thematics"] = json.dumps(THEMATICS)
        context["zones"] = json.dumps(ZONES)
        print("###", ZONES)
        context["selected_profile"] = request.GET.get("profile", "")
        print("###", context["profiles"])
        return context


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


class ContentPage(Page, FreeBodyField):
    class Meta:
        verbose_name = "Page de contenu"
        verbose_name_plural = "Pages de contenu"

    subpage_types: List[str] = []

    content_panels = Page.content_panels + FreeBodyField.panels


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
        return f"{pageurl({}, RessourcesPage.objects.get())}?profile={self.slug}"

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
