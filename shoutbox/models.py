from django.db import models
from django.utils.translation import ugettext as _
from community.models import Member


class ShoutBox(models.Model):
    name = models.CharField(_("name"), max_length=32)


class Shout(models.Model):
    shoutbox = models.ForeignKey(ShoutBox)
    created_by = models.ForeignKey(Member)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(_('body'))

    class Meta:
        ordering = "-created_at",
