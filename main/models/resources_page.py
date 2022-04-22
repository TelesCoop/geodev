import json
from typing import List

from django.forms import model_to_dict
from django.http import Http404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from main.constants import THEMATICS
from main.models.country import Country
from main.models.country import WorldZone
from main.models.models import Profile, ResourceType
from main.models.news import News
from main.models.resource import Resource


class ResourcesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des ressources"
        verbose_name_plural = "Pages des ressources"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

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
        context["resource_types"] = json.dumps(
            [model_to_dict(type_) for type_ in ResourceType.objects.all()]
        )
        context["zones"] = json.dumps(
            [model_to_dict(zone) for zone in WorldZone.objects.all()]
        )
        context["selected_profile"] = request.GET.get("profile", "")
        context["resources"] = json.dumps(
            [ressource.to_dict() for ressource in Resource.objects.all()]
        )
        context["countries"] = json.dumps(
            [country.to_dict() for country in Country.objects.all()]
        )
        return context
