# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django_bookmarks import settings
from django.template.loader import get_template
from django.template.context import Context
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

# Create your models here.
class Link(models.Model):
    url = models.URLField(unique=True)
    
    def __unicode__(self):
        return self.url

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.link.url)
    
    def get_absolute_url(self):
        return self.link.url
    
#    def colored_title(self):
#        return '<span style="color: #%s;">%s</span>' % (self.color_code, self.title)
#    colored_title.allow_tags = True
    
class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    # Tag 와 Bookmark 모델의 N:M 관계
    bookmarks = models.ManyToManyField(Bookmark)
    
    def __unicode__(self):
        return self.name

class SharedBookmark(models.Model):
    bookmark = models.ForeignKey(Bookmark, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(User)
    
    def __unicode__(self):
        return '%s, %s' % ( self.bookmark, self.votes )
    
class Friendship(models.Model):
    from_friend = models.ForeignKey( User, related_name = 'friend_set')
    to_friend = models.ForeignKey( User, related_name = 'to_friend_set')
    
    def __unicode__(self):
        return '%s, %s' % (
                           self.from_friend.username,
                           self.to_friend.username
                           )
        
    class Meta:
        unique_together = (('to_friend', 'from_friend'))
        
class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User)
    
    def __unicode__(self):
        return '%s, %s' % (self.sender.username, self.email)
    
    def send(self):
        subject = 'Welcome to Django bookmark service'
        link = 'http://%s/friend/accept/%s/' % (settings.SITE_HOST, self.code)
        template = get_template('invitation_email.txt')
        context = Context({
                            'name' : self.name,
                            'link' : link,
                            'sender' : self.sender.username,
                            })
        message = template.render(context)
        email = EmailMessage(subject, message, to=[self.email])
        email.send()
        