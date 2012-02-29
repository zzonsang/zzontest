from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from test_server import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

# admin
urlpatterns = patterns('admin',
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

# css, image, etc
urlpatterns += patterns('', 
     url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.site_media} ),
)

# weekly report application
urlpatterns += patterns('', 
    url(r'^', include('weekly_report.urls')),
)

