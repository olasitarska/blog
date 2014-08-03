from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('posts.urls', namespace='posts', app_name='posts')),
    (r'', include('users.urls', namespace='users', app_name='users')),
    (r'^admin/', include(admin.site.urls)),
)
