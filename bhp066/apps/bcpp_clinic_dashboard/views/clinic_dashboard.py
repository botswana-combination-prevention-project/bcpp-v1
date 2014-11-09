from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..classes import ClinicDashboard


@login_required
def clinic_dashboard(request, **kwargs):
    print "RegisteredSubject:"
    print kwargs.get('registered_subject')
    dashboard = ClinicDashboard(
        dashboard_type=kwargs.get('dashboard_type'),
        dashboard_id=kwargs.get('dashboard_id'),
        dashboard_model=kwargs.get('dashboard_model'),
        registered_subject=kwargs.get('registered_subject'),
        show=kwargs.get('show'),
        dashboard_type_list=['clinic'],
        )
    dashboard.set_context()
    return render_to_response(
        'clinic_dashboard.html',
        dashboard.context.get(),
        context_instance=RequestContext(request))
