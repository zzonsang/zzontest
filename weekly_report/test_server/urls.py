from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

site_media = os.path.join( os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('admin',
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('week_report', 
    url(r'^$', include('weekly_report.urls')),
)