from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

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
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^alm2map/', include(
                           'alm2map.urls', namespace='alm2map')),
                       url(r'^$', views.index),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.STATIC_ROOT}),
                       url(r'djide/', include('djide.urls')),
                       )\
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
#     static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
    urlpatterns += patterns('',
        (r'^tmp/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': '/tmp'}))
