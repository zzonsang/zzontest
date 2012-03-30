# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Report(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(verbose_name=u'Friday', default=datetime.now())
    content = models.TextField(verbose_name=u'Report')
    content_next = models.TextField(verbose_name=u'Plan')
        
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.date)
    
    def name(self):
        name = '%s%s' % (self.user.last_name, self.user.first_name)
        if name == "":
            return self.user.username
        return name
    
    class Meta:
        verbose_name = u"Weekly Report"
        unique_together = (('user', 'date'))
        permissions = (
                       ("view_reports", "Can see all reports"),
        )
        ordering = ['-date']
        
#    @staticmethod    
#    def autocomplete_search_field():
#        return ('id__iexact', 'content__icontains', )

class CustomFeed(models.Model):
    title = models.CharField(max_length=40)
    feed_url = models.URLField()
    limit = models.IntegerField()
    
    def __unicode__(self):
        return self.title