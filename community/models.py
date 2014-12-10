from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.db import models

GENDER_CHOICES = (
    ('f', _('female')),
    ('m', _('male')),
    ('t', _('timelord'))
)
class Member(AbstractUser):
    last_activity = models.DateTimeField(_('last activity'), null=True, blank=True)
    personal_text = models.TextField(_('personal text'), null=True, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, default='t')
    birth_date = models.DateField(_('date of birth'), null=True, blank=True)
    website = models.URLField(_('website'), max_length=256, blank=True, null=True)
    location = models.CharField(_('location'), max_length=100, null=True, blank=True)
    icq = models.CharField(_('icq'), max_length=14, null=True, blank=True)
    steam_id = models.CharField(_('steam id'), max_length=20, null=True, blank=True)
    signature = models.TextField(_('signature'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars', blank=True, null=True)
