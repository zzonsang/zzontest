from django.contrib import admin
from django_bookmarks.bookmarks.models import Link, Bookmark, Tag,\
    SharedBookmark, Friendship, Invitation
from django_bookmarks.bookmarks.admin_model import BookmarkAdmin

admin.site.register(Link, )

admin.site.register(Bookmark, BookmarkAdmin )

admin.site.register(Tag, )

admin.site.register(SharedBookmark, )

admin.site.register(Friendship, )

admin.site.register(Invitation, )