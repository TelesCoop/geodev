import json
from typing import List

from django.forms import model_to_dict
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.models import Page

from main.models import Thematic
from main.models.country import Country
from main.models.country import WorldZone
from main.models.models import Profile, ResourceType
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

        # Optimize Profile queries with prefetch_related for types
        profiles = Profile.objects.prefetch_related("types").all()

        context["profiles"] = json.dumps(
            {
                profile.slug: {"name": profile.name, "slug": profile.slug}
                for profile in profiles
            }
        )
        context["thematics"] = json.dumps(
            [thematic.to_dict() for thematic in Thematic.objects.all()]
        )
        context["resource_types"] = json.dumps(
            [model_to_dict(type_) for type_ in ResourceType.objects.all()]
        )
        context["zones"] = json.dumps(
            [zone.to_dict() for zone in WorldZone.objects.all()]
        )
        context["selected_profile"] = request.GET.get("profile", "")

        # Optimize Resource queries with all necessary prefetch_related and select_related
        resources = (
            Resource.objects.select_related("main_thematic")
            .prefetch_related(
                "profiles", "thematics", "countries__zone", "types", "zones"
            )
            .all()
        )

        context["resources"] = json.dumps(
            [ressource.to_dict() for ressource in resources]
        )

        # Optimize Country queries with select_related for zone
        context["countries"] = json.dumps(
            [
                country.to_dict()
                for country in Country.objects.select_related("zone").all()
            ]
        )

        # Use the already prefetched profiles to avoid additional queries
        context["resource_types_per_profile"] = json.dumps(
            {
                profile.slug: [type_.slug for type_ in profile.types.all()]
                for profile in profiles
            }
        )
        return context
