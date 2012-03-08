# -*- encoding: UTF-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django_bookmarks.bookmarks.views import main_page, user_page, logout_page, \
    register_page, bookmark_save_page, tag_page, tag_cloud_page, search_page,\
    bookmark_vote_page, popular_page, bookmark_page, ajax_tag_autocomplete,\
    friends_page, friend_add, friend_invite, friend_accept, highchart_page,\
    datatables_page, highchart_dynamic_page, datatables_bookmark_page
import os.path
from django.views.generic.simple import direct_to_template
from django_bookmarks.bookmarks.feeds import RecentBookmarks, UserBookmarks

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

site_media = os.path.join( os.path.dirname(__file__), 'site_media')

feeds = {
         'recent' : RecentBookmarks,
         'user' : UserBookmarks
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_bookmarks.views.home', name='home'),
    # url(r'^django_bookmarks/', include('django_bookmarks.foo.urls')),

    # Feed
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict' : feeds} ),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Main page
    url(r'^$', main_page),
    
    url(r'^popular/$', popular_page),
    
    # User page
    url(r'^user/(\w+)/$', user_page),

    # Login page
    url(r'^login/$', 'django.contrib.auth.views.login'),
    
    # Logout page
    url(r'^logout/$', logout_page),
    
    # css
    url(r'^site_media/(?P<path>.*)$', 
        'django.views.static.serve', {'document_root': site_media} ),
    
    # 가입 페이지 
    url(r'^register/$', register_page),
    
    # 가입 성공할 경우 보여주는 페이지
    url(r'^register/success/$', direct_to_template, {'template': 'registration/register_success.html'}),
    
    # 북마크 저장 페이지
    url(r'^save/$', bookmark_save_page),
    
    url(r'^vote/$', bookmark_vote_page),
    
    # 태그 페이지. 태그는 빈칸을 제외한 모든 문자를 허용한다.
    url(r'^tag/([^\s]+)/$', tag_page),
    
    # 태그 클라우드 페이지
    url(r'^tag/$', tag_cloud_page),
    
    # 검색 페이지 
    url(r'^search/$', search_page),
    
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^bookmark/(\d+)/$', bookmark_page),
    
    url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),
    
    url(r'^highchart/$', highchart_page), 
    url(r'^highchart/dynamic/$', highchart_dynamic_page),
    
    url(r'^datatables/$', datatables_page),
    url(r'^datatables/bookmark/$', datatables_bookmark_page),
)

urlpatterns += patterns('Comments', 
    url(r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('Friends', 
    url(r'^friends/(\w+)/$', friends_page),
    url(r'^friend/add/$', friend_add),
    url(r'^friend/invite/$', friend_invite),
    url(r'^friend/accept/(\w+)/$', friend_accept),
)


    
