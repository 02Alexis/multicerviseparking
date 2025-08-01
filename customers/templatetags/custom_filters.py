from django import template

register = template.Library()

@register.filter(name='format_license_plate')
def format_license_plate(value):
    if len(value) >= 6:
        return f"{value[:3]}-{value[3:]}"
    return value
