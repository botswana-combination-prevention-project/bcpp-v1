from bhp_context.classes import BaseContext

class Dashboard(object):
    
    context = BaseContext()
    
    def __init__(self, **kwargs):

        self.search_name = None    
        self.dashboard_type = None
        self.template = None

        self.search_name = kwargs.get('search_name', self.search_name)
        self.context.add(search_name = self.search_name ) 
        
    def create(self, **kwargs):

        self.dashboard_type = kwargs.get('dashboard_type', self.subject_type.lower())        
        
        self.template = kwargs.get('template', self.template)
        if not self.template:
            self.template = '%s_dashboard.html' % self.dashboard_type

        self.context.add(
            search_name = self.search_name,
            template = self.template,        
            dashboard_type = self.dashboard_type,
            )        

    def get_urlpatterns(self, view, regex):
        
        raise ValueError("Dashboard.get_urlpatterns() must be overridden")
        
    def get_context(self):
        return self.context.values        
