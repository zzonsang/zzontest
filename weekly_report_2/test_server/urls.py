from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^', include('vdi_report.urls')),
#        url(r'^grappelli/', include('grappelli.urls')),
        url(r'^admin_tools/', include('admin_tools.urls')),
)
