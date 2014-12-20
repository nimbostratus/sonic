from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.views.generic import FormView, View, ListView, UpdateView, DetailView
from django.utils.translation import ugettext as _

from community.forms import LoginForm, SignupForm
from community.models import Member


class SettingsView(UpdateView):
    template_name = 'community/settings.html'
    fields = ['first_name', 'last_name', 'email', 'about_me', 'mail_categories', 'mail_comments', 'bucket_threshold']
    success_url = reverse_lazy('community_list')

    def get_object(self, queryset=None):
        return Member.objects.get(pk=self.request.user.id)

    def form_valid(self, form):
        messages.info(self.request, _("Settings saved."))
        return super(SettingsView, self).form_valid(form)


class MemberDetailView(DetailView):
    template_name = 'community/member_detail.html'
    queryset = Member.objects.all()


class MemberListView(ListView):
    template_name = 'community/member_list.html'
    queryset = Member.objects.all()

    def get_queryset(self):
        member = Member.objects.all()
        sorting = self.kwargs.pop('sorting', None)
        if sorting is None:
            member = member.order_by('-id')
        elif sorting == 'nick':
            member = member.order_by('username')
        elif sorting == 'joined':
            member = member.order_by('date_joined')
        elif sorting == 'cash':
            member = member.order_by('cash')
        elif sorting == 'about_me':
            member = member.order_by('about_me')
        elif sorting == 'buckets':
            member = member.annotate(bucket_count=Count('bucket')).order_by('bucket_count')
        return member

class LoginView(FormView):
    template_name = 'community/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        member = form.get_member()
        if member is not None:
            login(self.request, member)
            messages.info(self.request, _('You are logged in now'))
        else:
            messages.error(self.request, _('unknown credentials'))
        return super(LoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _('You are logged out now.'))
        return HttpResponseRedirect(reverse_lazy('home'))


class SignupView(FormView):
    template_name = 'community/signup.html'
    success_url = reverse_lazy('home')
    form_class = SignupForm

    def form_valid(self, form):
        form.signup_member()
        messages.info(self.request, _('An activation mail was sent to you, follow the link in that mail.'))
        return super(SignupView, self).form_valid(form)


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        activation_hash_md5 = self.kwargs.get('activation_hash_md5')
        try:
            member = Member.objects.get(activation_hash_md5=activation_hash_md5)
            member.is_active = True
            member.activation_hash_md5 = None
            member.save()
            messages.info(request, _("Your account is now active. Have fun!"))
        except Member.DoesNotExist:
            messages.warning(request, _("Invalid activation key, please try to register again."))
        return HttpResponseRedirect(reverse_lazy('home'))
