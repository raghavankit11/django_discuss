from django import template

register = template.Library()

@register.filter
def remove_hash(value):
    return value.replace("#", "")

@register.filter
def is_user_subscribed(value, user_id):
    return value.subscriptions.filter(user__id__exact=user_id).exists()

@register.filter
def negate(value):
    return not value

@register.filter
def path(values):
    path_str = str()
    for index, p in enumerate(values):
        if index < len(values) - 1:
            path_str += p + '/'
        else:
            path_str += p

    return path_str

@register.filter
def path_till_index(values, till_index):
    path_str = str()
    for index, p in enumerate(values):
        if index < till_index - 1:
            path_str += p + '/'
    return path_str
