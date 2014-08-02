import datetime

from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def publish(self):
        self.published_date = datetime.datetime.now()
        self.save()
