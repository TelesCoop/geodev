from typing import List

from django.http import Http404
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page

from main.models.news import News


class NewsListPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = "Page des actualités"
        verbose_name_plural = "Pages des actualités"

    parent_page_types = ["main.HomePage"]
    subpage_types: List[str] = []
    max_count_per_parent = 1

    @route(r"^(.*)/$", name="news")
    def access_news_page(self, request, news_slug):
        try:
            news = News.objects.get(slug=news_slug)
        except (News.DoesNotExist, News.MultipleObjectsReturned):
            raise Http404
        return self.render(
            request,
            context_overrides={
                "news": news,
                # There is only one NewsListPage if there is only one language
                "news_page": NewsListPage.objects.first(),
            },
            template="main/news_page.html",
        )
