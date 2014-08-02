import datetime

from django.contrib.auth.models import User
from django.db import models

class PostManager(models.Manager):

    def get_query_set(self):

        return super(PostManager, self).get_query_set().filter(published_date__lte=datetime.datetime.now())


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now())
    published_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    published = PostManager()

    def __unicode__(self):
        return self.title

    def publish(self):
        self.published_date = datetime.datetime.now()
        self.save()
