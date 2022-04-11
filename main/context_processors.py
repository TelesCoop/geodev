from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from main.models import ResourcesPage


def general_context(_):
    context = {
        "resources_link": pageurl({}, ResourcesPage.objects.get()),
        "home_page": Page.objects.get(content_type__model="homepage"),
    }
    return context
