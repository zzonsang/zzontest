# -*- encoding: UTF-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.http import HttpResponse

class AdminBookmark(admin.ModelAdmin):
    list_display = ("title", "link", "user", )
    list_filter = ("user", )
    ordering = ("title", )
    search_fields = ("title", )
    
    def get_urls(self):
        urls = super(AdminBookmark, self).get_urls()
        my_urls = patterns('',
                           (r'^my_view/$', self.admin_site.admin_view(self.my_view))
                           )
        return my_urls + urls
    
    # 추가 페이지
    def my_view(self, request):
        return HttpResponse("Hello Custom Page")
    
    # 모델에 대한 View 제공
#    def change_view(self, request, object_id, extra_context=None):
#        return HttpResponse("Change View")