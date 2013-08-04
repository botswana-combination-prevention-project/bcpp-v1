from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bcpp_dashboard.classes import HouseholdDashboard


@login_required
def household_dashboard(request, **kwargs):
    dashboard = HouseholdDashboard()
    dashboard.set_template('householdstructure_dashboard.html')
    dashboard.create(**kwargs)
    return render_to_response(
        dashboard.get_template(),
        dashboard.get_context(),
        context_instance=RequestContext(request))
