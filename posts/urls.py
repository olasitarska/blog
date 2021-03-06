from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<post_pk>\d+)-(?P<slug>[-\.\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<post_pk>\d+)/edit/$', views.post_edit, name='post_edit'),

    url(r'^post/(?P<post_pk>\d+)/toggle_publish/$', views.post_toggle_publish, name='post_toggle_publish'),
    url(r'^post/(?P<post_pk>\d+)/remove/$', views.post_remove, name='post_remove'),
)
