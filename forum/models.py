from django.db import models
from django.utils.translation import ugettext as _
from community.models import Member


class Category(models.Model):
    name = models.CharField(_("category"), max_length=32)
    order = models.IntegerField(_('sort order'), default=0)

    def __unicode__(self):
        return self.name


class Board(models.Model):
    category = models.ForeignKey(Category)
    parent = models.ForeignKey('self', null=True, blank=True)
    order = models.IntegerField(_('sort order'), default=0)

    name = models.CharField(_("category"), max_length=120)
    description  = models.CharField(_("category"), max_length=250)

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    board = models.ForeignKey(Board)
    is_sticky = models.BooleanField(_('is sticky'), default=False)


class Post(models.Model):
    topic = models.ForeignKey(Topic)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    created_by = models.ForeignKey(Member, related_name="post_created_set", null=True, blank=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(Member, related_name="post_modified_set", blank=True, null=True)
    subject = models.CharField(_("category"), max_length=120)
    body = models.TextField(_('body'))
    icon = models.CharField(_('icon'), max_length=2, blank=True, null=True)
