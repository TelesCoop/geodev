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
    pass


class Map(Page):
    pass


class Ressource(TimeStampedModel):
    country = models.CharField(max_length=50, choices=COUNTRIES)
    name = models.CharField(max_length=100)
