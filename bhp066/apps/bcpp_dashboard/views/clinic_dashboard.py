from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.bcpp_clinic.models import ClinicConsent

from ..classes import ClinicDashboard


@login_required
def clinic_dashboard(request, **kwargs):
    dashboard = ClinicDashboard(
        dashboard_type=kwargs.get('dashboard_type'),
        dashboard_id=kwargs.get('dashboard_id'),
        dashboard_model=kwargs.get('dashboard_model'),
        registered_subject=kwargs.get('registered_subject'),
        show=kwargs.get('show'),
        dashboard_type_list=['clinic'],
        dashboard_models={'clinic_consent': ClinicConsent},
        app_label='bcpp_clinic',
        )
    dashboard.set_context()
    return render_to_response(
        'clinic_dashboard.html',
        dashboard.context.get(),
        context_instance=RequestContext(request))
