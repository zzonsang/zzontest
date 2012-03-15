# -*- encoding: UTF-8 -*-
from django.shortcuts import render_to_response
import logging
from django.template.context import RequestContext

logger = logging.getLogger('weekly_report')

'''
Admin 페이지에서 선택된 User에 대한 내용을 한번에 보여준다.
'''
def view_contents(modeladmin, request, queryset):
    
    logger.debug(queryset)
        
    
        
    variables = RequestContext(request, { 'reports' : queryset })
    
    for report in queryset:
        logger.debug(report.content_next)

    return render_to_response('view_content.html', variables)