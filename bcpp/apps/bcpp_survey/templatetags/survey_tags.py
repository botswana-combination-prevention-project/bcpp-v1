from django import template

from ..models import Survey

register = template.Library()


@register.filter(name='format_survey')
def format_survey(value):
    survey = Survey.objects.current_survey()
    if value == survey.survey_slug:
        value = '<font color="green">{}</font>'.format(value)
    else:
        value = '<I>{}</I>'.format(value)
    return value
