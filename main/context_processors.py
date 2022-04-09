from wagtail.core.templatetags.wagtailcore_tags import pageurl

from main.models import ResourcesPage


def general_context(request):
    context = {}
    context["resources_link"] = pageurl({}, ResourcesPage.objects.get())
    return context
