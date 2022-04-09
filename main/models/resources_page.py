import json
from typing import List

from django.http import Http404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from main.constants import THEMATICS, ZONES
from main.models.resource import Resource
from main.models.news import News
from main.models.models import Profile


class ResourcesPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des ressources"
        verbose_name_plural = "Pages des ressources"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="ressource")
    def access_ressource_page(self, request, news_slug):
        try:
            ressource = Resource.objects.get(slug=news_slug)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404
        return self.render(
            request,
            context_overrides={
                "ressource": ressource,
                # There is only one RessourcesPage if there is only one language
                "ressource_page": ResourcesPage.objects.first(),
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
        context["selected_profile"] = request.GET.get("profile", "")
        context["is_profile_locked"] = int(bool(request.GET.get("profile", False)))
        context["resources"] = json.dumps(
            [ressource.to_dict() for ressource in Resource.objects.all()]
        )

        # map data
        context["country_parameters"] = json.dumps(
            {"CM": {"lng": 13.6299563, "lat": 4.814121, "name": "Cameroun"}}
        )
        return context
