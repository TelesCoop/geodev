from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from main.models import ResourcesPage
from main.models.models import Profile
from main.models.news import News
from main.models.utils import SIMPLE_RICH_TEXT_FIELD_FEATURE


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["n_ressources"] = 148
        context["n_members"] = 80
        context["profiles"] = Profile.objects.all()
        context["resources_link"] = pageurl({}, ResourcesPage.objects.get())
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
