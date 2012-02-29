# -*- encoding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def main_page(request):
    return render_to_response("main_page.html", RequestContext(request))