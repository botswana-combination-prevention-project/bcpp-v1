from django.core.management.base import BaseCommand

from edc.subject.appointment_helper.classes import AppointmentHelper
from edc.subject.registration.models import RegisteredSubject
from edc.subject.appointment_helper.exceptions import AppointmentCreateError


class Command(BaseCommand):

    args = 'membership_model_name. Default is \'subjectconsent\''
    help = 'Generate missing appointments or do nothing if none are missing.'

    def handle(self, *args, **options):
        try:
            model_name = args[0]
        except IndexError:
            model_name = 'subjectconsent'
        appointment_helper = AppointmentHelper()
        options = {
            'model_name': model_name,
            'using': 'default',
            'base_appt_datetime': None,
            'dashboard_type': 'subject',
            'source': 'BaseAppointmentMixin',
            'visit_definitions': None,
            'verbose': True}

        for registered_subject in RegisteredSubject.objects.filter(subject_identifier__startswith='066'):
            print registered_subject
            try:
                appointments = appointment_helper.create_all(registered_subject, **options)
                for appointment in appointments:
                    print '  {}'.format(appointment)
            except AppointmentCreateError:
                pass
