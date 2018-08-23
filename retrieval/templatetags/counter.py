from django import template

register = template.Library()

def update_variable(curr_value, new_value):
    return new_value

register.filter('update_variable', update_variable)

