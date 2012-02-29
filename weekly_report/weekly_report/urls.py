# -*- encoding: UTF-8 -*-

from django.conf.urls.defaults import url, patterns
from weekly_report.views import main_page, logout_page, register_page,\
    weekly_report_save_page, user_page, user_report_page
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # main page
    url(r'^$', main_page),                   
    
    # login page
    url(r'^login/$', 'django.contrib.auth.views.login'),
    
    # Logout page
    url(r'^logout/$', logout_page),
    
    # Register page
    url(r'^register/$', register_page),
    
    # Success registration
    url(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
    
    # Save weekly repory
    url(r'^save/$', weekly_report_save_page),
    
    # User page
    url(r'^user/(\w+)/$', user_page),
    
    # Report page
    url(r'^user/(\w+)/report/(\d+)/$', user_report_page),
)