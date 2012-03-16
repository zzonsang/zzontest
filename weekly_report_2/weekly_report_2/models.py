# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(verbose_name='Friday')
#    title = models.CharField(max_length=100)
    content = models.TextField(verbose_name='Report')
    content_next = models.TextField(verbose_name='Plan')
#    date = models.DateTimeField(auto_now_add=True, verbose_name='')
        
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.date)
    
    class Meta:
        verbose_name = "Weekly Report"
        unique_together = (('user', 'date'))
        permissions = (
                       ("view_reports", "Can see all reports"),
        )
    
