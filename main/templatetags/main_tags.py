from django.template.defaulttags import register


@register.simple_tag()
def resource_page_url(resource):
    from main.models.resources_page import ResourcesPage

    try:
        resource_page = ResourcesPage.objects.get()
    except ResourcesPage.DoesNotExist:
        raise ResourcesPage.DoesNotExist("A RessourcePage must be created")
    url = resource_page.url + resource_page.specific.reverse_subpage(
        "resource",
        args=(str(resource.slug),),
    )
    return url


@register.simple_tag()
def news_page_url(news=None):
    from main.models.news_list_page import NewsListPage

    try:
        news_list_page = NewsListPage.objects.get()
    except NewsListPage.DoesNotExist:
        raise NewsListPage.DoesNotExist("A NewsListPage must be created")

    if news is None:
        return news_list_page.url
    url = news_list_page.url + news_list_page.reverse_subpage(
        "news",
        args=(str(news.slug),),
    )
    return url
