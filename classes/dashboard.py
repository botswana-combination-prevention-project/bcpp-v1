from django.core.exceptions import ImproperlyConfigured
from bhp_context.classes import BaseContext


class Dashboard(object):

    context = BaseContext()
    dashboard_identifier = None

    def __init__(self, **kwargs):

        self.search_name = None
        self._dashboard_type = None
        self._template = None

    def create(self, **kwargs):
        self.set_dashboard_type(kwargs.get('dashboard_type'))
        self.context.add(
            search_name=self.search_name,
            template=self.get_template(),
            dashboard_type=self.get_dashboard_type(),
            )

    def get_context_prep(self, **kwargs):
        pass

    def get_create_prep(self, **kwargs):
        pass

    def get_urlpatterns(self, view, regex):
        raise ValueError("Dashboard.get_urlpatterns() must be overridden")

    def get_context(self):
        return self.context.values

    def set_dashboard_type(self, value=None):
        self._dashboard_type = value

    def get_dashboard_type(self):
        if not self._dashboard_type:
            self.set_dashboard_type()
        return self._dashboard_type

    def set_template(self, value=None):
        self._template = value
        if not self._template and self.get_dashboard_type():
            self._template = '{0}_dashboard.html'.format(self.get_dashboard_type())
        if not self._template:
            raise TypeError('Attribute _template cannot be None.')

    def get_template(self):
        if not self._template:
            self.set_template()
        return self._template

    def get_url_patterns(self, view, regex, **kwargs):
        """Users must override."""
        raise ImproperlyConfigured('You need to define some dashboard urls.')
