# -*- encoding: UTF-8 -*-

from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.http import HttpResponse
import logging
from django.contrib.auth.models import User

logger = logging.getLogger('django.bookmark')

class BookmarkAdmin(admin.ModelAdmin):
    
    list_display = ("title", "link", "user", "__unicode__")
    list_filter = ("title","link","user__username" )
    ordering = ("title", )
    search_fields = ("title", )

    def get_urls(self):
        logger.debug("[call][get_urls(self)]")
        urls = super(BookmarkAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^my_view/$', self.admin_site.admin_view(self.my_view)),
#                           (r'^$', self.admin_site.admin_view(self.my_view)),
                           )
        return my_urls + urls
    
    # 추가 페이지
    def my_view(self, request):
        logger.debug("[call][my_view(self, request)]")
        return HttpResponse("Hello Custom Page")
    
    def queryset(self, request):
        logger.debug("[call][queryset(self, request]")
        qs = super(BookmarkAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    # 참고 : 접속한 유저만 할당할 수 있도록 함.
#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        logger.debug("[call][formfield_for_foreignkey] %s" % db_field.name )
#        if db_field.name == "user":
#            kwargs["queryset"] = User.objects.filter(username=request.user)
#        return super(BookmarkAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#    
#    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        logger.debug("[call][formfield_for_manytomany] %s" % db_field.name )
#        if db_field.name == "user":
#            kwargs["queryset"] = User.objects.filter()
#        return super(BookmarkAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
#    
    
            
            
    # 모델에 대한 View 제공
#    def change_view(self, request, object_id, extra_context=None):
#        return HttpResponse("Change View")
    
    # 되는 것들
#    search_fields = ("title", "user__username")
#    save_on_top = True
#    save_as = True
#    readonly_fields = ('title',)
#    raw_id_fields = ("user", )
#     fields = ('title','user','link')

#    fieldsets = (
#                 ( 'base', {'classes' : ['wide', 'extrapretty' ], 
#                            'fields' : ('title', 'user') } ),
#                 ( 'Advanced options', { 'classes' : ('collapse', ),
#                                        'fields' : ('link', ) 
#                                        }),
#    )

#    list_display_links = ("link", "user")
    
    ### 잘 안되는 것 들 
#    prepopulated_fields = {"slug" : ("title", )}
#    radio_fields = {"group": admin.VERTICAL}

