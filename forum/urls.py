from django.conf.urls import patterns, include, url
from django.contrib import admin
from forum.views import BoardView


urlpatterns = patterns('',
    url(r'^board/(?P<id>\d+)$', BoardView.as_view(), name="forum_board"),
    url(r'^admin/', include(admin.site.urls)),
)
