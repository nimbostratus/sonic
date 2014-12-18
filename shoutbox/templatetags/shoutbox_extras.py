from django.template import Library
from shoutbox.models import ShoutBox

register = Library()

@register.inclusion_tag('shoutbox/shoutbox.html')
def shoutbox(shoutbox_id, num_entries):
    return {
        'shoutbox': ShoutBox.objects.get(id=shoutbox_id),
        'num_entries': ":%s" % num_entries,
    }