from weekly_report.models import WReport
from weekly_report.admin_model import AdminWReport
from django.contrib import admin

admin.site.register(WReport, AdminWReport)