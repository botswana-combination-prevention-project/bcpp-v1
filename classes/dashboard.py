from bhp_context.classes import BaseContext


class Dashboard(object):

    context = BaseContext()
    dashboard_type = None
    template = None
    dashboard_identifier = None
    extra_url_context = None

    def __init__(self, **kwargs):

        self.search_name = None

    def create(self, **kwargs):

        if not self.dashboard_type:
            self.dashboard_type = kwargs.get('dashboard_type')
            if not self.dashboard_type:
                raise ValueError('%s requires a value for attribute dashboard_type.' % (self,))
        if not self.dashboard_identifier:
            self.dashboard_identifier = kwargs.get('dashboard_identifier')
            if not self.dashboard_identifier:
                raise ValueError('%s requires a value for attribute dashboard_identifier. Perhaps set this in the view.' % (self,))
        if not self.template:
            self.template = kwargs.get('template', '%s_dashboard.html' % self.dashboard_type)
        if not self.extra_url_context:
            self.extra_url_context = kwargs.get('extra_url_context', {})
        self.context.add(
            search_name=self.search_name,
            template=self.template,
            dashboard_type=self.dashboard_type,
            dashboard_identifier=self.dashboard_identifier,
            extra_url_context=self.extra_url_context,
            )

    def get_context_prep(self, **kwargs):
        pass

    def get_create_prep(self, **kwargs):
        pass

    def get_urlpatterns(self, view, regex):
        raise ValueError("Dashboard.get_urlpatterns() must be overridden")

    def get_context(self):
        return self.context.values
