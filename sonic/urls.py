from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings
from forum.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^forum/', include('forum.urls')),
    url(r'^community/', include('community.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
