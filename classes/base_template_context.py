from django.conf import settings
from bhp_common.utils import os_variables


class BaseContext(dict):

    """Descriptor for the default template context"""

    def __init__(self, **kwargs):
        self._context = {}
        defaults = {
            'extend': "base_site.html",  # required, but this default will avoid an error
            'template': "",  # required
            'report_title': "",
            'section_name': "",
            'os_variables': os_variables,
            'sql': "",
            'database': settings.DATABASES['default'],
            }
        self._context.update(**defaults)
        #section_name, for example 'clinic', 'lab', 'admin', 'surveys' comes as a parameter from the Url
        if kwargs.get('section_name') is None:
            raise TypeError('BaseSearch requires keyword/value for key \'section_name\'. None given.')
        else:
            self._context['section_name'] = kwargs.get('section_name')

    @property
    def context(self):
        return self._context
