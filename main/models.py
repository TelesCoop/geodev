import json
from django.db import models
from main.countries import COUNTRIES

from wagtail.core.models import Page


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
        context["profiles"] = [
            {
                "name": "décideurs",
                "description": """Élu local ou gestionnaire de territoire, accédez aux
                    produits, services et tableaux de bord, documents
                    de synthèse pour
                    <span class="has-text-weight-bold">aider vos prises de décision</span>.""",
                "link": "/ressources",
                "link_text": "Voir les ressources",
            },
            {
                "name": "géomaticiens",
                "description": """Cartographe ou gestionnaire de bases de données géographiques,
                        accédez aux produits, applications et documents techniques pour
                    <span class="has-text-weight-bold">faciliter et enrichir vos travaux</span>.""",
                "link": "/ressources",
                "link_text": "Voir les ressources",
            },
            {
                "name": "Télédétecteurs",
                "description": """Vous traitez des images satellitaires pour proposer
                        des services et vos projets de recherche,
                        <span class="has-text-weight-bold">
                            accédez plus facilement aux images disponibles, outils de traitement,
                            formations et ressources bibliographiques
                        </span>.""",
                "link": "/ressources",
                "link_text": "Voir les ressources",
            },
        ]
        context["news_list"] = [
            {
                "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
                "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
                "date": "06.03.2022",
                "link": "/news/1",
                "image": "/static/img/home-intro-image.svg",
            },
            {
                "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
                "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
                "date": "06.03.2022",
                "link": "/news/1",
                "image": "/static/img/home-intro-image.svg",
            },
            {
                "title": "Utilisations de la télédétection pour le suivi des forêts et eaux",
                "summary": "Un atelier de réflexion entre la coordination de l’ART et les responsables de Centres d’Expertise Scientifique (CES) du Pôle Theia a eu lieu dans les locaux du CESBIO, à Toulouse le 1er octobre (...)",
                "date": "06.03.2022",
                "link": "/news/1",
                "image": "/static/img/home-intro-image.svg",
            },
        ]
        context["newsletter_link"] = "newsletter-link"
        return context


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


class Ressource(TimeStampedModel):
    country = models.CharField(max_length=50, choices=COUNTRIES)
    name = models.CharField(max_length=100)
