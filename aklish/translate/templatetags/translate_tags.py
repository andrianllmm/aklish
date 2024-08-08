from django import template
register = template.Library()


@register.filter
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def get_user_vote(translation, user):
    if user.is_authenticated:
        return translation.votes.get_or_create(translation=translation, user=user)[0]
    return None