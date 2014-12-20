from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from community.views import LoginView, SignupView, ActivateView, LogoutView, MemberListView, SettingsView, \
    MemberDetailView


urlpatterns = patterns(
    '',
    url(r'^$', login_required(MemberListView.as_view()), name='community_list'),
    url(r'^(?P<pk>\d+)$', login_required(MemberDetailView.as_view()), name='community_detail'),
    url(r'^sort/(?P<sorting>[A-Za-z0-9_]+)$', login_required(MemberListView.as_view()), name="community_list"),
    url(r'^settings$', login_required(SettingsView.as_view()), name='community_settings'),
    url(r'^login$', LoginView.as_view(), name='community_login'),
    url(r'^logout$', login_required(LogoutView.as_view()), name='community_logout'),
    url(r'^signup$', SignupView.as_view(), name='community_signup'),
    url(r'^activate/(?P<activation_hash_md5>[a-zA-Z0-9]{32})$', ActivateView.as_view(), name='community_activate'),
    )

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^change-password/$', 'password_change',
        {
            'template_name': 'community/password_change.html',
            'post_change_redirect': 'community_change_password_done'
        },
        name="community_change_password"),

    url(r'^change-password/done/$', 'password_change_done',
        {
            'template_name': 'community/password_change_done.html',
            },
        name='community_change_password_done'),


    url(r'^password-reset/$', 'password_reset',
        {
            'template_name': 'community/password_reset_form.html',
            'email_template_name': 'community/password_reset_email.html',
            'post_reset_redirect': 'community_reset_password_done',
            },
        name="community_reset_password"),

    url(r'^password-reset-done/$', 'password_reset_done',
        {
            'template_name': 'community/password_reset_done.html'
        },
        name="community_reset_password_done"),

    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', 'password_reset_confirm',
        {
            'template_name': 'community/password_reset_confirm.html',
            'post_reset_redirect': 'community_reset_password_complete',
            },
        name="community_reset_password_confirm"),

    url(r'^password-reset-complete/$', 'password_reset_complete',
        {
            'template_name': 'community/password_reset_complete.html'
        },
        name="community_reset_password_complete"),
    )
