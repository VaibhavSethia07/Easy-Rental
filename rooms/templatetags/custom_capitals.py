from django import template

register = template.Library()

@register.filter()
def custom_capitals(value):
    return value.capitalize()