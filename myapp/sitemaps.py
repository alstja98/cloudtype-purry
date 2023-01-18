from django.urls import reverse
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['openbeta']

    def location(self, item):
        return reverse(item)