import inspect
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import get_model, Max
from bhp_visit.models import VisitDefinition, ScheduleGroup
from bhp_visit.classes import VisitDefinitionHelper
from django.core.exceptions import ImproperlyConfigured
from appointment_datetime import AppointmentDatetime
from bhp_appointment.models import Appointment, Holiday, Configuration


class AppointmentManager(object):
    """ """
    def __init__(self):
        pass

    def create_all(self, **kwargs):
        """Creates appointments for a registered subject based on a list of visit definitions if given model_name is a member of a schedule group.

            1. Only create for visit_instance = 0
            2. If appointment exists, just update the appt_datetime
        """
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError('AppointmentMaker.create_appointments requires registered_subject. Got None')
        # this is the model of the membership_form
        model_name = kwargs.get("model_name")
        if not model_name:
            raise TypeError('AppointmentMaker.create_appointments requires a model_name. Got None')
        # this is the model of the membership_form
        dashboard_type = kwargs.get("dashboard_type", None)
        if not model_name:
            raise TypeError('AppointmentMaker.create_appointments requires dashboard_type. Got None')
        # base_appt_datetime must come from the membership_form model and not from the appt_datetime
        # of the first appointment as the user may change this.
        # base_appt_datetime = kwargs.get("base_appt_datetime")
        if ScheduleGroup.objects.filter(membership_form__content_type_map__model=model_name):
            # get list of visits for scheduled group containing this model
            # get schedule_group
            schedule_group = ScheduleGroup.objects.get(membership_form__content_type_map__model=model_name)
            # get membership_form of this schedule_group for this registered_subject
            membership_form_model = get_model(app_label=schedule_group.membership_form.content_type_map.app_label, model_name=model_name)
            if membership_form_model.objects.filter(registered_subject=registered_subject):
                # in some cases, send the base_appt_datetime, such as when
                # the visit_datetime is a next appt datetime.
                # But ideally, it is better to get this from
                # get_registration_datetime() on the model.
                base_appt_datetime = kwargs.get('base_appt_datetime', None)
                if not base_appt_datetime:
                    # determine base_appt_datetime using the membership_form instance
                    # for an existing membership form
                    membership_form = membership_form_model.objects.get(registered_subject=registered_subject)
                    base_appt_datetime = membership_form.get_registration_datetime()
            elif kwargs.get('base_appt_datetime'):
                # ??? can you get here??
                # i guess you could pass the base_appt_datetime from the call
                base_appt_datetime = kwargs.get('base_appt_datetime')
            else:
                # we may be calling this method as a new membership form is being inserted
                # once the instance is saved, the created attribute will = datetime.today()
                #base_appt_datetime = datetime.today()

                # i have decided that it is safer for the model_instance to return the
                # base_appt_datetime instead of assuming datetime.today(),
                # thus, the model save() method must have been called already.
                # ...see BaseRegisteredSubjectModel.save()
                # so if you get here throw an error.
                raise AttributeError("%s method %s cannot determine the registration model_instance. "
                                     "This is needed to call get_registration_datetime()." % (self, inspect.stack()[0][3],))
            visit_definitions = VisitDefinition.objects.filter(schedule_group=schedule_group)
            appointment_datetime = AppointmentDatetime()
            for visit_definition in visit_definitions:
                # calculate the appointment date
                if visit_definition.time_point == 0:
                    #appt_datetime = self.best_appointment_datetime(appt_datetime=base_appt_datetime)
                    appt_datetime = appointment_datetime.get(base_appt_datetime)
                else:
                    appt_datetime = self.next_appointment_datetime(visit_definition, base_appt_datetime)
                # if appt exists, update appt_datetime
                if Appointment.objects.filter(
                            registered_subject=registered_subject,
                            visit_definition=visit_definition,
                            visit_instance=0):
                    appt = Appointment.objects.get(
                                registered_subject=registered_subject,
                                visit_definition=visit_definition,
                                visit_instance=0)
                    appt.appt_datetime = appt_datetime
                    appt.save()
                # else create a new appointment
                else:
                    Appointment.objects.create(
                        registered_subject=registered_subject,
                        visit_definition=visit_definition,
                        visit_instance=0,
                        appt_datetime=appt_datetime,
                        timepoint_datetime=appt_datetime,
                        dashboard_type=dashboard_type)

    def delete_appointments_for_instance(self, model_instance):
        """ Delete appointments for this registered_subject for this model_instance but only if visit report not yet submitted """
        #visit_definitions = self.list_visit_definitions_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())
        visit_definitions = VisitDefinitionHelper.list_all_for_model(model_instance.registered_subject, model_instance._meta.object_name.lower())

        # only delete appointments without a visit model
        appointments = Appointment.objects.filter(registered_subject=model_instance.registered_subject, visit_definition__in=visit_definitions)
        count = 0
        visit_model = model_instance.get_visit_model(model_instance)
        for appointment in appointments:
            if not visit_model.objects.filter(appointment=appointment):
                appointment.delete()
                count += 1
        return count

    def create_next_instance(self, **kwargs):
        """ Creates the next instance of an appointment given the base appointment instance (.0) and the next appt_datetime """
        appointment = kwargs.get('base_appointment')
        next_appt_datetime = kwargs.get('next_appt_datetime')
        # check if there are rules to determine a better appt_datetime
        appt_datetime = self.best_appointment_datetime(appt_datetime=next_appt_datetime)
        if not Appointment.objects.filter(
            registered_subject=appointment.registered_subject,
            visit_definition=appointment.visit_definition,
            appt_datetime=next_appt_datetime):
            aggr = Appointment.objects.filter(
                registered_subject=appointment.registered_subject,
                visit_definition=appointment.visit_definition
                ).aggregate(Max('visit_instance'))
            if aggr:
                next_visit_instance = int(aggr['visit_instance__max'] + 1.0)
                Appointment.objects.create(
                    registered_subject=appointment.registered_subject,
                    visit_definition=appointment.visit_definition,
                    visit_instance=next_visit_instance,
                    appt_datetime=appt_datetime)

    def list_appointments_for_model(self, registered_subject, model_name):
        """ Lists created appointments for this registered_subject for this model_name """
        #visit_definitions = self.list_visit_definitions_for_model(registered_subject, model_name)
        visit_definitions = VisitDefinitionHelper.list_all_for_model(registered_subject, model_name)
        return Appointment.objects.filter(registered_subject=registered_subject, visit_definition__in=visit_definitions)

    def next_appointment_datetime(self, visit_definition, base_appt_datetime):
        """ Returns the appt_datetime given the visit_definition and base_appt_datetime"""
        # should be date from membership form
        appt_datetime = base_appt_datetime + VisitDefinition.objects.relativedelta_from_base(visit_definition=visit_definition)
        appt_datetime = self.best_appointment_datetime(appt_datetime, base_appt_datetime.isoweekday())
        return appt_datetime

    def best_appointment_datetime(self, appt_datetime, weekday=None):
        appointment_datetime = AppointmentDatetime()
        return appointment_datetime.get(appt_datetime, weekday)
