# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

class WReport(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.title)
    