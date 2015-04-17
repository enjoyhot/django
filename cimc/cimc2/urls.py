from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from hello.views import index,user_review,device_review,middleware_review,kvm_manage,server_info,cimc_login,cimc_logout
from servers.views import servers_list
from instance.views import instances
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cimc2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # django management background, not used
    url(r'^admin/', include(admin.site.urls)),

    url(r'^cimc/logout','hello.views.cimc_logout',name='cimc-logout'),
    url(r'^cimc/login', 'hello.views.cimc_login',name='cimc-login'),
    url(r'^cimc/index.html', 'hello.views.index',name='index'),
    url(r'^cimc/user-review.html','hello.views.user_review',name='user-review'),
    url(r'^cimc/device-review.html$','hello.views.device_review',name='device-review'),
    url(r'^cimc/middleware-review.html$','hello.views.middleware_review',name='middleware-review'),

    # kvm manager
    url(r'^cimc/kvm-manage.html$','hello.views.kvm_manage',name='kvm-manage'),
    url(r'^cimc/server-info.html$', 'hello.views.server_info',name='server-info'),
    url(r'^cimc/servers','servers.views.servers_list',name='servers_list'),
    url(r'^cimc/cpu-mem','hello.cpu_mem.cpu_mem',name='server-cpumem'),
    url(r'^cimc/get-status','hello.server_info.get_status',name='get-status'),
    url(r'^cimc/instance/(\d+)/([\w\-\.]+)/$', 'instance.views.instance', name='instance'),
    url(r'^cimc/instances/(\d+)/$', 'instance.views.instances',name='instances'),
    url(r'^cimc/create/(\d+)/$', 'create.views.create', name='create'),
    url(r'^cimc/host/(\d+)/$', 'hostdetail.views.overview', name='overview'),
    url(r'^cimc/storages/(\d+)/$', 'storages.views.storages', name='storages'),
    url(r'^cimc/storage/(\d+)/([\w\-\.]+)/$', 'storages.views.storage', name='storage'),
    url(r'^cimc/networks/(\d+)/$', 'networks.views.networks', name='networks'),
    url(r'^cimc/network/(\d+)/([\w\-\.]+)/$', 'networks.views.network', name='network'),
    url(r'^cimc/interfaces/(\d+)/$', 'interfaces.views.interfaces', name='interfaces'),
    url(r'^cimc/interface/(\d+)/([\w\.]+)$', 'interfaces.views.interface', name='interface'),
    url(r'^cimc/secrets/(\d+)/$', 'secrets.views.secrets', name='secrets'),
    url(r'^cimc/info/hostusage/(\d+)/$', 'hostdetail.views.hostusage', name='hostusage'),
    url(r'^cimc/info/insts_status/(\d+)/$', 'instance.views.insts_status', name='insts_status'),
    url(r'^cimc/info/instusage/(\d+)/([\w\-\.]+)/$', 'instance.views.instusage', name='instusage'),
    url(r'^cimc/console/$', 'console.views.console', name='console'),
    url(r'^infrastructure/$', 'servers.views.infrastructure', name='infrastructure'),
 
)
#urlpatterns += patterns(
#    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#)
urlpatterns += patterns('', 
    (r'^i18n/', include('django.conf.urls.i18n')), 
 )
#urlpatterns += staticfiles_urlpatterns()
