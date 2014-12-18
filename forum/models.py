from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import QuerySet, Count
from django.utils.translation import ugettext as _
from community.models import Member


class Category(models.Model):
    name = models.CharField(_("category"), max_length=32)
    order = models.IntegerField(_('sort order'), default=0)

    class Meta:
        ordering = '-order',

    def __unicode__(self):
        return self.name


class BoardQuerySet(models.QuerySet):
    def get_top_level(self):
        return self.filter(parent__isnull=True)


class Board(models.Model):
    objects = BoardQuerySet.as_manager()

    category = models.ForeignKey(Category)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="child_set")
    order = models.IntegerField(_('sort order'), default=0)

    name = models.CharField(_("category"), max_length=120)
    description  = models.CharField(_("category"), max_length=250)

    class Meta:
        ordering = '-order',

    def get_absolute_url(self):
        return reverse('forum_board', kwargs={'id': self.id})

    def __unicode__(self):
        return self.name


class TopicQuerySet(QuerySet):
    def get_post_count(self):
        return self.aggregate(Count('post'))['post__count']


class Topic(models.Model):
    objects = TopicQuerySet.as_manager()

    board = models.ForeignKey(Board)
    is_sticky = models.BooleanField(_('is sticky'), default=False)

    class Meta:
        ordering = '-id',

    def get_latest_post(self):
        return self.post_set.latest('id')

    def get_absolute_url(self):
        return reverse('forum_topic', kwargs={'board_id': self.board.id, 'topic_id': self.id })


class Post(models.Model):
    topic = models.ForeignKey(Topic)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    created_by = models.ForeignKey(Member, related_name="post_created_set", null=True, blank=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True, blank=True, null=True)
    modified_by = models.ForeignKey(Member, related_name="post_modified_set", blank=True, null=True)
    subject = models.CharField(_("category"), max_length=120)
    body = models.TextField(_('body'))
    icon = models.CharField(_('icon'), max_length=12, blank=True, null=True)

    class Meta:
        ordering = 'created_at',


class Attachment(models.Model):
    image = models.ImageField(_('image'), upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)


