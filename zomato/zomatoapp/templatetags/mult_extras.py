from django import template

register = template.Library()

@register.filter()
def mult(value1,value2):
    return (float(value1)*float(value2))
