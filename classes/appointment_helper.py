import inspect
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
#from bhp_visit.classes import VisitDefinitionHelper
from appointment_date_helper import AppointmentDateHelper


class AppointmentHelper(object):

    def create_all(self, registered_subject, model_name, base_appt_datetime=None, dashboard_type=None, source=None):
        """Creates appointments for a registered subject based on a list of visit definitions if given model_name is a member of a schedule group.

            Args:
                registered_subject: current subject
                model_name: model of the membership_form
                dashboard_type:

            1. Only create for visit_instance = 0
            2. If appointment exists, just update the appt_datetime

            visit_definition contains schedule group contains membership form
        """
        # base_appt_datetime must come from the membership_form model and not from the appt_datetime
        # of the first appointment as the user may change this.
        appointments = []
        if source != 'BaseAppointmentMixin':  # just a temporary check to ensure this is called by the signal
            raise ImproperlyConfigured('AppointmentHelper.create_all() may only be called from BaseAppointmentMixin.')
        if ScheduleGroup.objects.filter(membership_form__content_type_map__model=model_name):
            schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model=model_name)
            membership_form_model = schedule_group.membership_form.content_type_map.model_class()
            if membership_form_model.objects.filter(registered_subject=registered_subject).exists():
                # found an existing membership form ...
                # need base_appt_datetime. if not passed, such as when the visit_datetime is a
                # next appt datetime, get from get_registration_datetime() on this model.
                if not base_appt_datetime:
                    # determine base_appt_datetime using this membership_form instance
                    membership_form = membership_form_model.objects.get(registered_subject=registered_subject)
                    base_appt_datetime = membership_form.get_registration_datetime()
            else:
                # not found, which is supposed to be impossible -- this is called in post_save signal.
                raise ImproperlyConfigured("Cannot get the membership_form_model instance. Expected to find an instance of model {0} belonging to schedule group {1}.".format(membership_form_model, schedule_group))
            visit_definitions = VisitDefinition.objects.filter(schedule_group=schedule_group)
            appointment_date_helper = AppointmentDateHelper()
            Appointment = get_model('bhp_appointment', 'appointment')
            if not visit_definitions:
                raise ImproperlyConfigured('No visit_definitions found for membership form class {0} in schedule group {1}. Expected at least one visit definition to be associated with schedule group {1}.'.format(membership_form_model, schedule_group))
            for visit_definition in visit_definitions:
                # calculate the appointment date for new appointments
                if visit_definition.time_point == 0:
                    appt_datetime = appointment_date_helper.get_best_datetime(base_appt_datetime, registered_subject.study_site)
                else:
                    appt_datetime = appointment_date_helper.get_relative_datetime(base_appt_datetime, visit_definition)
                # get or create an appointment for this visit definition
                defaults = {
                    'appt_datetime': appt_datetime,
                    'timepoint_datetime': appt_datetime,
                    'dashboard_type': dashboard_type}
                appointment, created = Appointment.objects.get_or_create(
                    registered_subject=registered_subject,
                    visit_definition=visit_definition,
                    visit_instance='0',
                    defaults=defaults)
                if not created:
                    td = appointment.best_appt_datetime - appt_datetime
                    if abs(td.total_seconds()) > 59:
                        # the calculated appointment date does not match the best_appt_datetime (not within 59 seconds)
                        # which means you changed the date on the membership form and now
                        # need to correct the best_appt_datetime
                        appointment.appt_datetime = appt_datetime
                        appointment.best_appt_datetime = appt_datetime
                        appointment.save()
                appointments.append(appointment)
        return appointments

    def delete_for_instance(self, model_instance):
        """ Delete appointments for this registered_subject for this model_instance but only if visit report not yet submitted """
        #visit_definitions = self.list_visit_definitions_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())
        visit_definitions = VisitDefinition.objects.list_all_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())
        Appointment = get_model('bhp_appointment', 'appointment')
        # only delete appointments without a visit model
        appointments = Appointment.objects.filter(registered_subject=model_instance.registered_subject, visit_definition__in=visit_definitions)
        count = 0
        visit_model = model_instance.get_visit_model_cls(model_instance)
        # find the most recent visit model instance and delete any appointments after that
        for appointment in appointments:
            if not visit_model.objects.filter(appointment=appointment):
                appointment.delete()
                count += 1
        for appointment in appointments:
            if not visit_model.objects.filter(appointment=appointment):
                appointment.delete()
                count += 1
        return count

    def create_next_instance(self, base_appointment_instance, next_appt_datetime):
        """ Creates a continuation appointment given the base appointment instance (.0) and the next appt_datetime """
        appointment = base_appointment_instance
        Appointment = get_model('bhp_appointment', 'appointment')
        if not Appointment.objects.filter(
            registered_subject=appointment.registered_subject,
            visit_definition=appointment.visit_definition,
            appt_datetime=next_appt_datetime):
            aggr = Appointment.objects.filter(
                registeredsubject=appointment.registered_subject,
                visit_definition=appointment.visit_definition
                ).aggregate(Max('visit_instance'))
            if aggr:
                appointment_date_helper = AppointmentDateHelper()
                # check if there are rules to determine a better appt_datetime
                appt_datetime = appointment_date_helper.get_best_datetime(next_appt_datetime, appointment.registered_subject.study_site)
                next_visit_instance = int(aggr['visit_instance__max'] + 1.0)
                Appointment.objects.create(
                    registered_subject=appointment.registered_subject,
                    visit_definition=appointment.visit_definition,
                    visit_instance=str(next_visit_instance),
                    appt_datetime=appt_datetime)
