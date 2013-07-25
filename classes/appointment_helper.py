from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
from appointment_date_helper import AppointmentDateHelper
from bhp_subject_config.models import SubjectConfiguration
from bhp_appointment.models import Configuration
from bhp_appointment.exceptions import AppointmentStatusError


class AppointmentHelper(object):

    def create_all(self, registered_subject, model_name, using=None, base_appt_datetime=None, dashboard_type=None, source=None):
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
        default_appt_type = self._get_default_appt_type(registered_subject)
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
                    'dashboard_type': dashboard_type,
                    'appt_type': default_appt_type}
                appointment, created = Appointment.objects.using(using).get_or_create(
                    registered_subject=registered_subject,
                    visit_definition=visit_definition,
                    visit_instance='0',
                    defaults=defaults)
                if not created:
                    td = appointment.best_appt_datetime - appt_datetime
                    if td.days == 0 and abs(td.seconds) > 59:
                        # the calculated appointment date does not match the best_appt_datetime (not within 59 seconds)
                        # which means you changed the date on the membership form and now
                        # need to correct the best_appt_datetime
                        appointment.appt_datetime = appt_datetime
                        appointment.best_appt_datetime = appt_datetime
                        appointment.save(using)
                appointments.append(appointment)
        return appointments

    def delete_for_instance(self, model_instance, using=None):
        """ Delete appointments for this registered_subject for this model_instance but only if visit report not yet submitted """
        #visit_definitions = self.list_visit_definitions_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())
        visit_definitions = VisitDefinition.objects.list_all_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())
        Appointment = get_model('bhp_appointment', 'appointment')
        # only delete appointments without a visit model
        appointments = Appointment.objects.using(using).filter(registered_subject=model_instance.registered_subject, visit_definition__in=visit_definitions)
        count = 0
        visit_model = model_instance.get_visit_model_cls(model_instance)
        # find the most recent visit model instance and delete any appointments after that
        for appointment in appointments:
            if not visit_model.objects.using(using).filter(appointment=appointment):
                appointment.delete()
                count += 1
        for appointment in appointments:
            if not visit_model.objects.using(using).filter(appointment=appointment):
                appointment.delete()
                count += 1
        return count

    def create_next_instance(self, base_appointment_instance, next_appt_datetime, using=None):
        """ Creates a continuation appointment given the base appointment instance (.0) and the next appt_datetime """
        appointment = base_appointment_instance
        Appointment = get_model('bhp_appointment', 'appointment')
        if not Appointment.objects.using(using).filter(
            registered_subject=appointment.registered_subject,
            visit_definition=appointment.visit_definition,
            appt_datetime=next_appt_datetime):
            aggr = Appointment.objects.using(using).filter(
                registeredsubject=appointment.registered_subject,
                visit_definition=appointment.visit_definition
                ).aggregate(Max('visit_instance'))
            if aggr:
                appointment_date_helper = AppointmentDateHelper()
                # check if there are rules to determine a better appt_datetime
                appt_datetime = appointment_date_helper.get_best_datetime(next_appt_datetime, appointment.registered_subject.study_site)
                next_visit_instance = int(aggr['visit_instance__max'] + 1.0)
                Appointment.objects.using(using).create(
                    registered_subject=appointment.registered_subject,
                    visit_definition=appointment.visit_definition,
                    visit_instance=str(next_visit_instance),
                    appt_datetime=appt_datetime)

    def check_appt_status(self, appointment, using):
        """Checks the appt_status relative to the visit tracking form and ScheduledEntryBucket.
        """
        from bhp_entry.classes import ScheduledEntry
        # for an existing appointment, check if there is a visit tracking form already on file
        if not appointment.visit_definition.visit_tracking_content_type_map:
            raise ImproperlyConfigured('Unable to determine the visit tracking model. Update bhp_visit.visit_definition {0} and select the correct visit model.'.format(appointment.visit_definition))
        if not appointment.visit_definition.visit_tracking_content_type_map.model_class().objects.filter(appointment=appointment):
            # no visit tracking, can only be New or Cqncelled
            if appointment.appt_status not in ['new', 'cancelled']:
                appointment.appt_status = 'new'
        else:
            # have visit tracking, can only be Done, Incomplete, In Progress
            visit_model_instance = appointment.visit_definition.visit_tracking_content_type_map.model_class().objects.get(appointment=appointment)
            #if visit_model_instance.reason in visit_model_instance.get_visit_reason_no_follow_up_choices():
            if not ScheduledEntry().show_scheduled_entries(appointment.registered_subject, visit_model_instance=visit_model_instance):
                # visit reason implies no data will be collected, so set appointment to Done
                appointment.appt_status = 'done'
            else:
                ScheduledEntryBucket = get_model('bhp_entry', 'ScheduledEntryBucket')
                # set to in progress, if not already set
                if appointment.appt_status in ['done', 'incomplete']:
                    # test if Done or Incomplete
                    if ScheduledEntryBucket.objects.filter(appointment=appointment, entry_status='NEW').exists():
                        #objs = ScheduledEntryBucket.objects.filter(appointment=appointment, entry_status='NEW')
                        appointment.appt_status = 'incomplete'
                    else:
                        appointment.appt_status = 'done'
                elif appointment.appt_status in ['new', 'cancelled', 'in_progress']:
                    appointment.appt_status = 'in_progress'
                    # only one appointment can be "in_progress", so look for any others in progress and change
                    # to Done or Incomplete, depending on ScheduledEntryBucket (if any NEW => incomplete)
                    ScheduledEntryBucket = get_model('bhp_entry', 'ScheduledEntryBucket')
                    for appt in appointment.__class__.objects.filter(registered_subject=appointment.registered_subject, appt_status='in_progress').exclude(pk=appointment.pk):
                        if ScheduledEntryBucket.objects.filter(appointment=appt, entry_status='NEW').exists():
                            # there are NEW forms
                            if appt.appt_status != 'incomplete':
                                appt.appt_status = 'incomplete'
                                # call raw_save to avoid coming back to this method.
                                appt.raw_save(using)
                        else:
                            # all forms are KEYED or NOT REQUIRED
                            if appt.appt_status != 'done':
                                appt.appt_status = 'done'
                                # call raw_save to avoid coming back to this method.
                                appt.raw_save(using)
                else:
                    raise AppointmentStatusError('Did not expect appt_status == \'{0}\''.format(appointment.appt_status))
        return appointment

    def _get_default_appt_type(self, registered_subject):
        default_appt_type = None
        if SubjectConfiguration.objects.filter(subject_identifier=registered_subject.subject_identifier):
            default_appt_type = SubjectConfiguration.objects.get(subject_identifier=registered_subject.subject_identifier).default_appt_type
        if not default_appt_type:
            default_appt_type = Configuration.objects.get_configuration().default_appt_type
        return default_appt_type
