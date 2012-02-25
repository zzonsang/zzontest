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
    '''
    추가로 전달되는 정보가 들어오면 이 메서드를 호출한다.
    예를 들어, ^feeds/user/$ 라는 URL과 연결되어 있다면, ^feeds/user/param1/param2/$ 
    요청은 ['param1', 'param2'] 이라는 추가 정보를 처리한다.
    
    변수를 받아 User 객체를 반환한다. 없으면 404 페이지를 만든다.
    '''
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username=bits[0])
    
    '''
    RecentBookmarks 에서는 클래스의 속성을 이용한 것이고,
    여기서는 메서드로 처리하는 것이다.
    '''
    def title(self, user):
        return u'Django bookmark | Registerd bookmark of %s' % user.username
    
    def link(self, user):
        return '/feeds/user/%s/' % user.username
    
    def description(self, user):
        return u'Bookmark is a registered Django bookmark he was through.' % user.username
    
    '''
    User 객체를 받아서 북마크 목록을 반환한다.
    '''
    def items(self, user):
        return user.bookmark_set.order_by('-id')[:10]
    