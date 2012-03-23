from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import os

admin.autodiscover()

site_media = os.path.join( os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
#     Uncomment the admin/doc line below to enable admin documentation:
     url(r'^doc/', include('django.contrib.admindocs.urls')),
#     Uncomment the next line to enable the admin:
     url(r'', include(admin.site.urls)),
     
     url(r'^grappelli/', include('grappelli.urls')),
     
      # css
     url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media} ),
)
