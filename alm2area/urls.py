from django.conf.urls import patterns, url

from alm2area import views

urlpatterns = patterns('',
                       url(
                           r'^$',
                           views.alm_form_view,
                           name='index',
                       ),
                       url(
                           r'^processing/',
                           views.alm_form_view,
                           name='processing',
                       ),
)
