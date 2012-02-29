# -*- encoding: UTF-8 -*-
from django.conf.urls.defaults import url, patterns
from weekly_report.views import main_page

urlpatterns = patterns('weekly_report',
    url(r'^$', main_page),                   


)