from django.conf.urls import patterns, url
from .view1 import room_for_rent_list, room_for_rent_detail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^room_for_rent/$', 'room_for_rent_list'),
    url(r'^room_for_rent/(?P<pk>[0-9]+)/$', 'room_for_rent_detail'),
)


urlpatterns = format_suffix_patterns(urlpatterns)
