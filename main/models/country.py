from django.db import models
from django.forms import model_to_dict
from wagtail.search import index
from wagtail.search.index import Indexed
from wagtail.snippets.models import register_snippet


@register_snippet
class WorldZone(models.Model):
    class Meta:
        verbose_name = "zone du monde"
        verbose_name_plural = "zones du monde"

    name = models.CharField(verbose_name="Nom", max_length=60)
    code = models.CharField(verbose_name="code (ne pas changer !)", max_length=20)

    def __str__(self):
        return self.name


@register_snippet
class Country(models.Model, Indexed):
    class Meta:
        verbose_name = "pays"
        verbose_name_plural = "pays"

    name = models.CharField(verbose_name="Nom", max_length=60)
    code = models.CharField(verbose_name="code à deux lettres", max_length=20)
    latitude = models.FloatField(verbose_name="latitude du centre")
    longitude = models.FloatField(verbose_name="longitude du centre")
    zone = models.ForeignKey(WorldZone, on_delete=models.SET_NULL, null=True)

    search_fields = [
        index.SearchField("name", partial_match=True),
        index.SearchField("code", partial_match=True),
    ]

    def __str__(self):
        return self.name

    def to_dict(self):
        to_return = model_to_dict(self)
        to_return["zone"] = self.zone.code if self.zone else None
        return to_return
