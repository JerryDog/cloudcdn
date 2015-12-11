from django.conf.urls import patterns, include, url
from cdn_manage import views
from django.contrib import admin

admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'cdn.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', views.index, name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^switch_project/$', views.switch_project, name='switch_project'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^index_map/$', views.index_map, name='index_map'),
                       url(r'^domain_manage/$', views.domain_manage, name='domain_manage'),
                       url(r'^delete_domain/$', views.delete_domain, name='delete_domain'),
                       url(r'^edit_domain/(\d+)/$', views.edit_domain, name='edit_domain'),
                       url(r'^update_domain/(\d+)/$', views.update_domain, name='update_domain'),
                       url(r'^handler_cache/$', views.handler_cache, name='handler_cache'),
                       url(r'^bandwidth/$', views.bandwidth, name='bandwidth'),
                       url(r'^flow_value/$', views.flow_value, name='flow_value'),
                       url(r'^bandwidth_csv/$', views.bandwidth_csv, name='bandwidth_csv'),
)

if settings.DEBUG is False:
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT,
                                }),
    )