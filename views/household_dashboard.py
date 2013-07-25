from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_appointment.models import Appointment
from bhp_registration.models import RegisteredSubject
from bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard
from bcpp_survey.models import Survey
from bcpp_household.models import Household
from bcpp_household_member.models import HouseholdMember
from bcpp_subject.models import SubjectVisit


@login_required
def household_dashboard(request, **kwargs):
    #dashboard_type = kwargs.get('dashboard_type', None)
    #if dashboard_type != 'household':
    #    raise TypeError('Expected dashboard_type to be \'household\'. Got {0}'.format(dashboard_type))
    if kwargs.get('household_identifier'):
        household_identifier = kwargs.get('household_identifier')
    #elif kwargs.get('pk'):
    #    household_identifier = Household.objects.get(pk=kwargs.get('pk')).household_identifier
    else:
        household_identifier = None
    survey = kwargs.get('survey')
    #section_name = kwargs.get('section_name', 'household')
    #search_type =  kwargs.get('search_type', 'household')
    search_term =  kwargs.get('search_term', None)
    # create dashboard object
    dashboard = HouseholdDashboard(**kwargs)
    # create a basic dashboard context
    dashboard.create(
        dashboard_type='household',
        household_identifier=household_identifier,
        survey=survey,
        template='householdstructure_dashboard.html',
        first_name=kwargs.get('first_name'))
    # TODO: adding this here manually but this should come from the section class
    dashboard.context.add(
        section_name=kwargs.get('section_name', 'household'),
        search_type=kwargs.get('search_type', 'household'))
    return render_to_response(
        dashboard.template,
        dashboard.get_context(),
        context_instance=RequestContext(request))
