from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cmb import views
import cmb.settings as settings
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'cmb.views.home', name='home'),
                       # url(r'^cmb/', include('cmb.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/',
                       # include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^%sadmin/'%(settings.URL_PREFIX), include(admin.site.urls)),
                       url(r'^%salm2area/'%(settings.URL_PREFIX), include(
                           'alm2area.urls', namespace='alm2area')),
                       url(r'^%s$'%(settings.URL_PREFIX), include(
                           'alm2area.urls', namespace='alm2area')),
                       url(r'%sdjide/'%(settings.URL_PREFIX), include('djide.urls')),
                       ) + staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += patterns('',
        (r'^tmp/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': '/tmp'}))
