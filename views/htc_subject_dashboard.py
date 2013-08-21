from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bcpp_dashboard.classes import HtcSubjectDashboard


@login_required
def htc_subject_dashboard(request, **kwargs):
    dashboard = HtcSubjectDashboard()
    dashboard.set_template('htc_subject_dashboard.html')
    dashboard.create(**kwargs)
    return render_to_response(
        dashboard.get_template(),
        dashboard.get_context(),
        context_instance=RequestContext(request))
