from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.bcpp_dashboard.classes import HtcSubjectDashboard


@login_required
def htc_subject_dashboard(request, **kwargs):
    dashboard = HtcSubjectDashboard(
        dashboard_type=kwargs.get('dashboard_type'),
        dashboard_id=kwargs.get('dashboard_id'),
        dashboard_model=kwargs.get('dashboard_model'),
        registered_subject=kwargs.get('registered_subject'),
        show=kwargs.get('show'),
        dashboard_type_list=['htc_subject'],
        #dashboard_models={'subject_consent': SubjectConsent},
        )
    dashboard.set_context()
    return render_to_response(
        'htc_subject_dashboard.html',
        dashboard.get_context().get(),
        context_instance=RequestContext(request))
