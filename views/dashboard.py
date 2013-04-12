from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_registration.models import RegisteredSubject
from bcpp_dashboard.classes import SubjectDashboard
from bcpp_subject.models import SubjectConsent


@login_required
def dashboard(request, **kwargs):

    if kwargs.get('dashboard_type') == 'subject':
        subject_consent = None
        if kwargs.get('subject_identifier'):
            subject_identifier = kwargs.get('subject_identifier')
        elif kwargs.get('pk'):
            if SubjectConsent.objects.get(pk=unicode(kwargs.get('pk'))).exists():
                subject_consent = SubjectConsent.objects.get(pk=unicode(kwargs.get('pk')))
        elif kwargs.get('registered_subject'):
            registered_subject = RegisteredSubject.objects.get(pk=kwargs.get('registered_subject'))
            subject_identifier = registered_subject.subject_identifier
        else:
            subject_identifier = ''
        if RegisteredSubject.objects.filter(subject_identifier=subject_identifier).exists():
            registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
        dashboard = SubjectDashboard(**kwargs)
        dashboard.create(
            registered_subject=registered_subject,
            visit_code=kwargs.get('visit_code'),
            visit_instance=kwargs.get("visit_instance"))
#        dashboard.context.add(
#            subject_consent=subject_consent)
    else:
        raise ValueError('Unknown dashboard_type, must be \'subject\'. Got %s' % kwargs.get('dashboard_type'))
    return render_to_response(
        dashboard.template,
        dashboard.get_context(),
        context_instance=RequestContext(request))
