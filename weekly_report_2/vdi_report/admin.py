# -*- encoding: UTF-8 -*-
from django.contrib import admin
from vdi_report.models import Report, CustomFeed
from django.contrib.auth.models import User
from vdi_report.admin_action import view_contents, export_excel_contents
from django.contrib.sites.models import Site

'''
Report 모델에 대한 Admin 모델 
'''
class ReportAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "content", "content_next", )
    list_display_links = ("user", "content", "content_next", "date")
    list_filter = ("user__username", "date")
    
    def queryset(self, request):
        qs = super(ReportAdmin, self).queryset(request)
        # 팀장 권한이 있다면 팀원들 것이 모두 보이도록 수정   
#        if request.user.is_superuser:
        if request.user.has_perm('vdi_report.view_reports'):
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(username=request.user)
        return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
   
    def get_actions(self, request):
        actions = super(ReportAdmin, self).get_actions(request)
        
        if not request.user.has_perm('vdi_report.view_reports'):
            if 'View_Contents' in actions:
                del actions['View_Contents']
        return actions
     
class CustomFeedAdmin(admin.ModelAdmin):   
    list_display = ('title', 'feed_url', 'limit',)
    list_display_links = ('title', 'feed_url', 'limit',)
    list_filter = ('title', )
            
'''
Model 등록
'''            
admin.site.register(Report, ReportAdmin),
admin.site.register(CustomFeed, CustomFeedAdmin),

'''
Model 제거 
'''
admin.site.unregister(Site)

'''
Action 등록 
'''
admin.site.add_action(view_contents, 'View_Contents')
admin.site.add_action(export_excel_contents, 'Export_Excel_Contents')

