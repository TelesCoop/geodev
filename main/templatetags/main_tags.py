from django.template.defaulttags import register


@register.simple_tag()
def ressource_page_url(ressource_page, ressource):
    url = ressource_page.url + ressource_page.specific.reverse_subpage(
        "ressource",
        args=(str(ressource.slug),),
    )
    return url


@register.simple_tag()
def news_page_url(news_list_page, news):
    url = news_list_page.url + news_list_page.reverse_subpage(
        "news",
        args=(str(news.slug),),
    )
    return url
