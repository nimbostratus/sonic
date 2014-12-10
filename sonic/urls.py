from django.conf.urls import patterns, url, include
from forum.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^forum/', include('forum.urls')),
)
