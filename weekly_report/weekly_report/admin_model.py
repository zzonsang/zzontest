from django.contrib import admin

class AdminWReport(admin.ModelAdmin):
    list_display = ("user", "title", "date")