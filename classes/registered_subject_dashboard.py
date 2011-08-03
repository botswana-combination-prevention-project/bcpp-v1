from bhp_dashboard.classes import Dashboard

class RegisteredSubjectDashboard(Dashboard):

    def create(self, **kwargs):

        # call super to initialize default context 
        super(RegisteredSubjectDashboard, self).create(**kwargs)

        # to see default context, and therefore which variables are already
        # available to you, see ContextDescriptor in bhp_dashboard.classes.Dashboard or
        # raise TypeError(self.context)
        
        # add extra context specific to this dashboard
    


