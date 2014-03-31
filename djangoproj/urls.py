from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'djangoproj.views.index', name='index'),
    url(r'^backlog/', include('backlog.urls', namespace="backlog")),
    # url(r'^$', )
    url(r'^admin/', include(admin.site.urls)),
)
