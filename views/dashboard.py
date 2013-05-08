from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_appointment.models import Appointment
from bhp_registration.models import RegisteredSubject
from bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard
from bcpp_survey.models import Survey
from bcpp_household.models import Household, HouseholdStructureMember
from bcpp_subject.models import SubjectVisit


@login_required
def dashboard(request, **kwargs):
    """ Shit """
    if kwargs.get('dashboard_type') == 'subject':
        if kwargs.get('household_structure_member'):
            household_structure_member = HouseholdStructureMember.objects.get(pk=kwargs.get('household_structure_member'))
            if RegisteredSubject.objects.filter(registration_identifier=household_structure_member.internal_identifier).exists():
                # this is the first hsm entry so registration_identifier=hsm.pk
                registered_subject = RegisteredSubject.objects.get(registration_identifier=household_structure_member.internal_identifier)
                subject_identifier = registered_subject.registration_identifier
            else:
                raise ValueError('bcpp_survey.views.dashboard expects all household_structure_members to have an entry in RegisterSubject. Got None for %s.' % (household_structure_member,))
        elif kwargs.get('pk'):
            household_structure_member = HouseholdStructureMember.objects.get(pk=kwargs.get('pk'))
            if RegisteredSubject.objects.filter(registration_identifier=household_structure_member.internal_identifier).exists():
                # this is the first hsm entry so registration_identifier=hsm.pk
                registered_subject = RegisteredSubject.objects.get(registration_identifier=household_structure_member.internal_identifier)
                subject_identifier = registered_subject.registration_identifier
            else:
                raise ValueError('bcpp_survey.views.dashboard expects all household_structure_members to have an entry in RegisterSubject. Got None for %s.' % (household_structure_member,))
        elif kwargs.get('appointment'):
            # if coming from the visit model link in the appointment row
            appointment = Appointment.objects.get(pk=kwargs.get('appointment'))
            survey = Survey.objects.get(survey_slug=kwargs.get('survey'))
            registered_subject = appointment.registered_subject
            subject_identifier = registered_subject.registration_identifier
            household_structure_member = HouseholdStructureMember.objects.get(internal_identifier=registered_subject.registration_identifier, survey__survey_slug=survey.survey_slug)
        elif kwargs.get('subject_identifier') and kwargs.get('visit_code'):
            #raise TypeError()
            subject_identifier = kwargs.get('subject_identifier')
            visit_code = kwargs.get('visit_code')
            subject_visit = SubjectVisit.objects.get(appointment__registered_subject__subject_identifier=subject_identifier, appointment__visit_definition__code=visit_code)
            kwargs.update({'visit_instance': subject_visit.appointment.visit_instance})
            kwargs.update({'appointment': subject_visit.appointment})
            household_structure_member = subject_visit.household_structure_member
            survey = household_structure_member.survey.survey_slug
            registered_subject = RegisteredSubject.objects.get(registration_identifier=household_structure_member.internal_identifier)
            subject_identifier = registered_subject.registration_identifier
        elif kwargs.get('subject_identifier') and not kwargs.get('visit_code'):
            registered_subject = RegisteredSubject.objects.get(subject_identifier=kwargs.get('subject_identifier'))
            household_structure_member = HouseholdStructureMember.objects.get(registered_subject=registered_subject)
            #household_structure_member = HouseholdStructureMember.objects.get(internal_identifier=registered_subject.registration_identifier)
            #survey = household_structure_member.survey.survey_slug
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        elif kwargs.get('registered_subject') or (kwargs.get('subject_identifier') and not kwargs.get('visit_code')):
            registered_subject = RegisteredSubject.objects.get(pk=kwargs.get('registered_subject'))
            household_structure_member = None
            #household_structure_member = HouseholdStructureMember.objects.get(internal_identifier=registered_subject.registration_identifier)
            #survey = household_structure_member.survey.survey_slug
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        elif kwargs.get('registration_identifier'):
            registration_identifier = kwargs.get('registration_identifier')
            registered_subject = RegisteredSubject.objects.get(registration_identifier=registration_identifier)
            household_structure_member = None
            #household_structure_member = HouseholdStructureMember.objects.get(internal_identifier=registration_identifier)
            #survey = household_structure_member.survey.survey_slug
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        else:
            raise ValueError('dashboard view needs a value for attribute \'household_structure_member\'.')
        if not household_structure_member:
            raise ValueError('dashboard view needs a value for attribute \'household_structure_member\'.')
        dashboard = SubjectDashboard(**kwargs)
        # create a basic dashboard context
        kwargs.update({'registered_subject': registered_subject})
        kwargs.update({'household_structure_member': household_structure_member})
        kwargs.update({'subject_consent': household_structure_member.consent()})
        kwargs.update({'extra_url_context': '&household_structure_member={household_structure_member}&survey={survey}'.format(household_structure_member=household_structure_member.pk,
                                                                                                                              survey=household_structure_member.survey.survey_slug,)})
        dashboard.create(**kwargs)
    elif kwargs.get('dashboard_type') == 'household':
        if kwargs.get('household_identifier'):
            household_identifier = kwargs.get('household_identifier')
        elif kwargs.get('pk'):
            household_identifier = Household.objects.get(pk=kwargs.get('pk')).household_identifier
        else:
            household_identifier = None
        survey = kwargs.get('survey')
        # create dashboard object
        dashboard = HouseholdDashboard(**kwargs)
        # create a basic dashboard context
        dashboard.create(
            dashboard_type='household',
            household_identifier=household_identifier,
            survey=survey,
            first_name=kwargs.get('first_name'))
    else:
        raise ValueError('Unknown dashboard_type, must be \'subject\' or \'household\'. Got %s' % kwargs.get('dashboard_type'))
    return render_to_response(
        dashboard.template,
        dashboard.get_context(),
        context_instance=RequestContext(request))
