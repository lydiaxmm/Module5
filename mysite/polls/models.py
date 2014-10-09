import datetime
from django.utils import timezone
from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    start_date = models.DateTimeField('date started')
    end_date = models.DateTimeField('date ended')
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now
    
    def notexpired(self):
        now = timezone.now()
        return now <=self.end_date
    
    def hasstarted(self):
        now = timezone.now()
        return now >=self.start_date
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text
