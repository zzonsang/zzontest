from weekly_report.models import Report
from weekly_report.admin_model import AdminWReport
from django.contrib import admin

admin.site.register(Report, AdminWReport)