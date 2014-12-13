from django.conf.urls import patterns, include, url
from django.contrib import admin
from forum.views import BoardView, TopicView


urlpatterns = patterns(
    '',
    url(r'^board/(?P<id>\d+)$', BoardView.as_view(), name="forum_board"),
    url(r'^board/(?P<board_id>\d+)/topic/(?P<topic_id>\d+)$', TopicView.as_view(), name="forum_topic"),
    url(r'^admin/', include(admin.site.urls)),
)
