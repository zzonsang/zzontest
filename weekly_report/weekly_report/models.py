# -*- encoding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

month_list = ( 
         ('1','Jan'),
         ('2', 'Feb'),
         ('3', 'Mar'),
         ('4', 'Apr'),
         ('5', 'May'),
         ('6', 'Jun'),
         ('7', 'Jul'),
         ('8', 'Aug'),
         ('9', 'Sep'),
         ('10', 'Oct'),
         ('11', 'Nov'),
         ('12', 'Dec'),          
        )

week_list = (
             ('1', '1 week'),
             ('2', '2 week'),
             ('3', '3 week'),
             ('4', '4 week'),
             ('5', '5 week'),             
             ) 

class Report(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    month = models.CharField(max_length=10)
    week = models.CharField(max_length=10)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.title)
    