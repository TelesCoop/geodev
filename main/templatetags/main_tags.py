from django.template.defaulttags import register

from main.models import NewsListPage, RessourcesPage


@register.simple_tag()
def ressource_page_url(ressource):
    try:
        ressource_page = RessourcesPage.objects.get()
    except RessourcesPage.DoesNotExist:
        raise RessourcesPage.DoesNotExist("A RessourcePage must be created")
    url = ressource_page.url + ressource_page.specific.reverse_subpage(
        "ressource",
        args=(str(ressource.slug),),
    )
    return url


@register.simple_tag()
def news_page_url(news):
    try:
        news_list_page = NewsListPage.objects.get()
    except NewsListPage.DoesNotExist:
        raise NewsListPage.DoesNotExist("A NewsListPage must be created")
    url = news_list_page.url + news_list_page.reverse_subpage(
        "news",
        args=(str(news.slug),),
    )
    return url
