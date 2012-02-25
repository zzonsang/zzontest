from django.contrib import admin

class AdminBookmark(admin.ModelAdmin):
    list_display = ("title", "link", "user", )
    list_filter = ("user", )
    ordering = ("title", )
    search_fields = ("title", )
    