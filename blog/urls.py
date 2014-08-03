from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('posts.urls', namespace='posts', app_name='posts')),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    (r'^admin/', include(admin.site.urls)),
)
