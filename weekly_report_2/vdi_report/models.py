# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(verbose_name=u'Friday')
#    title = models.CharField(max_length=100)
    content = models.TextField(verbose_name=u'Report')
    content_next = models.TextField(verbose_name=u'Plan')
#    date = models.DateTimeField(auto_now_add=True, verbose_name='')
        
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.date)
    
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
