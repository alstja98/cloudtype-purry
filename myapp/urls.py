from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *
from django.views.generic import TemplateView

sitemaps = { 'static': StaticViewSitemap, }

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('app1/', include('core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt',  TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]
