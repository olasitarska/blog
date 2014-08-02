import datetime

from django.contrib.auth.models import User
from django.db import models

class PostManager(models.Manager):
    def get_query_set(self):
        return super(PostManager, self).get_query_set().filter(published_date__isnull=False, published_date__lte=datetime.datetime.now())


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=datetime.datetime.now())
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=200)

    objects = models.Manager()
    published = PostManager()

    def __unicode__(self):
        return self.title

    def publish(self):
        self.published_date = datetime.datetime.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()

    def is_public(self):
        if self.published_date:
            if self.published_date < datetime.datetime.now():
                return True
        return False
