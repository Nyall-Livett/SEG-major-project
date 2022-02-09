from django import template

register = template.Library()

@register.filter(name='render_buttons')
def render_buttons(value, arg):
    if arg == value:
        return True
    return False

@register.filter(name='render_icon')
def render_icon(value):
    if  value == 0:
        return "bi-people"
    elif  value == 1:
        return "bi-clock"
    elif  value == 2 or value == 3 or value == 4:
        return "bi-book"
