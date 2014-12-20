import hashlib
import random

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from community.models import Member


class LoginForm(forms.Form):
    username = forms.CharField(label=_('username'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput())

    def get_member(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        # try to get the user by email address
        if user is None:
            try:
                user = authenticate(username=Member.objects.get(email=username, password=password))
            except Member.DoesNotExist:
                user = None

        if user is not None and user.is_active == True:
            return user
        return None


class SignupForm(forms.Form):
    username = forms.CharField(label=_('username'))
    email = forms.EmailField(label=_('email'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput())
    password_repeat = forms.CharField(label=_('repeat password'), widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            Member.objects.get(username=username)
        except Member.DoesNotExist:
            return username
        else:
            raise ValidationError(_('The username is already taken.'))

    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password_repeat'):
            raise ValidationError(_('The passwords do not match'))

    def signup_member(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        activation_hash_md5 = hashlib.md5(username + email + str(random.randint(0, 200000))).hexdigest()

        member = Member.objects.create_user(username, email, password, activation_hash_md5=activation_hash_md5)
        member.is_active = False
        member.save()

        member.email_user(
            _('Fun-Metal-Bucket: Registration'),
            render_to_string(
                'community/signup_mail.txt',
                {
                    'member': member,
                    'base_url': settings.BASE_URL,
                    }
            ))
