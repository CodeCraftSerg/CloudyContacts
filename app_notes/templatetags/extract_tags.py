from django import template

register = template.Library()


@register.filter(name='tag_filter')
def tag_filter(tags):
    if isinstance(tags, str):
        return tags.split(',')
    elif hasattr(tags, 'all'):
        return ', '.join(tag.name for tag in tags.all())
    else:
        return tags