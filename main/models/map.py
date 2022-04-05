import json

from wagtail.core.models import Page


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
