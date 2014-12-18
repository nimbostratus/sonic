from django.template import Library

register = Library()


@register.inclusion_tag('forum/_pagination.html', takes_context=True)
def pagination(context):
    context.update(dict(page_range=range(1, context['page_obj'].paginator.num_pages + 1)))
    return context