from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),
)
