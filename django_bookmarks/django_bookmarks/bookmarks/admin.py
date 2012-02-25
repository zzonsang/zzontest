from django.contrib import admin
from django_bookmarks.bookmarks.models import Link, Bookmark, Tag,\
    SharedBookmark
from django_bookmarks.bookmarks.admin_model import AdminBookmark

admin.site.register(Link, )

admin.site.register(Bookmark, AdminBookmark )

admin.site.register(Tag, )

admin.site.register(SharedBookmark, )