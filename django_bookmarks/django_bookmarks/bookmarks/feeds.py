# -*- conding: UTF-8 -*-
from django.contrib.syndication.feeds import Feed
from django_bookmarks.bookmarks.models import Bookmark
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class RecentBookmarks(Feed):
    title = u'Django bookmark | Rencent bookmark'
    link =  '/feeds/recent/'
    description = u'Django bookmark services through the registered bookmarks'
    
    def items(self):
        return Bookmark.objects.order_by('-id')[:10]
    
class UserBookmarks(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])
    
    def title(self, user):
        return u'Django bookmark | Registerd bookmark of %s' % ( user.username )
    
    def link(self, user):
        return '/feeds/user/%s/' % ( user.username )
    
    def description(self, user):
        return u'Bookmark is a registered Django bookmark %s was through.' % ( user.username )
    
    def items(self, user):
        return user.bookmark_set.order_by('-id')[:10]
    