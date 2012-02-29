# -*- encoding: UTF-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import logout
from weekly_report.forms import RegistrationForm, ReportSaveForm
from django.contrib.auth.models import User
from weekly_report.models import Report
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 10

def main_page(request):
    return render_to_response("main_page.html", RequestContext(request))

def logout_page(request):
    # session logout
    logout(request)
    
    # Redirect 을 '/'로 지정함
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1']
                                            )
            
            return HttpResponseRedirect('/register/success')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    
    return render_to_response('registration/register.html', RequestContext(request, variables))


def weekly_report_save_page(request):        
    ajax = request.GET.has_key('ajax')
    if request.method == 'POST':
        form = ReportSaveForm(request.POST)
        if form.is_valid():
            report = _report_save_page(request, form)
            return HttpResponseRedirect('/user/%s/' % request.user.username)
    else:
        form = ReportSaveForm()
        
    variables = RequestContext(request, {'form': form} )    
    return render_to_response('report_save.html', variables)
            
def _report_save_page(request, form):       
    report = Report.objects.get_or_create(
                                           user=request.user, 
                                           title=form.cleaned_data['title'],
                                           content=form.cleaned_data['content']
                                           )
    
    return report
        
def user_page(request, username):      
    user = get_object_or_404(User, username=username)
    query_set = user.report_set.order_by('-id')
    paginator = Paginator(query_set, ITEMS_PER_PAGE)
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    try:
        reports = paginator.page(page)
    except:
        raise Http404
    
    variables = RequestContext(request, {
                                         'reports': reports.object_list,
                                         'username': username,
                                         'show_user' : True,
                                         'show_paginator': paginator.num_pages > 1,
                                         'has_prev': reports.has_previous(),
                                         'has_next': reports.has_next(),
                                         'page': page,
                                         'pages': paginator.num_pages,
                                         'next_page' : reports.next_page_number(),
                                         'prev_page' : reports.previous_page_number(),
                                         })
    return render_to_response('user_page.html', variables)
    
def user_report_page(request, username, reportid):    
    reports = Report.objects.filter(user__username__exact=username, id=reportid)
    
    if reports.count() == 1:
        variables = RequestContext(request, {
                                             'report' : reports[0],
                                             'username' : username,
                                             'reportid' : reportid
                                             })
        return render_to_response('user_report.html', variables)
    
    else:
        return HttpResponseRedirect('/')
    