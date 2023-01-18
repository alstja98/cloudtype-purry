from django.urls import reverse
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'openbeta']

    def location(self, item):
        return reverse(item)