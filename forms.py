from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from bhp_entry.models import ScheduledEntryBucket
from bhp_appointment.models import Appointment
from bhp_dispatch.helpers import is_dispatched_registered_subject


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

    def clean(self):

        cleaned_data = self.cleaned_data
        if cleaned_data.get('registered_subject', None):
            registered_subject = cleaned_data.get('registered_subject')
            dispatched, producer_name = is_dispatched_registered_subject(registered_subject)
            if dispatched:
                raise forms.ValidationError("Data for {0} is currently dispatched to netbook {1}. "
                                 "This form may not be modified.".format(registered_subject.subject_identifier,
                                                                          producer_name))
        appt_datetime = cleaned_data.get("appt_datetime")
        if not appt_datetime:
            raise forms.ValidationError('Appointment date and time are required')
        appt_status = cleaned_data.get("appt_status")
        registered_subject = cleaned_data.get("registered_subject")
        visit_definition = cleaned_data.get("visit_definition")
        visit_instance = cleaned_data.get("visit_instance")
        #default_entry_status = cleaned_data.get('default_entry_status')

        # do not create an appointment unless visit_code+visit_instance=0 already exists
        # visit_instance 0 visits should be created automatically
        # create appointment link is just for creating continuation appointment
        if visit_instance == 0:
            raise ValidationError('Continuation appointment may not have visit instance equal to 0.')
        elif not Appointment.objects.filter(
                registered_subject=registered_subject,
                visit_definition=visit_definition,
                visit_instance=0).exists():
            raise ValidationError('Cannot create continuation appointment for visit %s. Cannot find the original appointment (visit instance equal to 0).' % (visit_definition,))
        else:
            pass
        # check appointment date relative to status
        # postive t1.days => is a future date [t1.days > 0]
        # negative t1.days => is a past date [t1.days < 0]
        # zero t1.days => now (regardless of time) [t1.days == 0]
        t1 = appt_datetime.date() - date.today()
        if appt_status == 'cancelled':
            pass
        elif appt_status == 'incomplete':
            pass
        elif appt_status == 'done':
            # must not be future
            if t1.days > 0:
                raise forms.ValidationError("Status is 'done' so the appointment date cannot be a future date. You wrote '%s'" % appt_datetime)
            # cannot be done if no visit report, but how do i get to the visit report??
            # cannot be done if bucket entries exist that are 'new'
            if Appointment.objects.filter(
                registered_subject=registered_subject,
                #appt_status = 'in_progress',
                visit_definition=visit_definition,
                visit_instance=visit_instance).exists():
                appointment = Appointment.objects.get(registered_subject=registered_subject,
                    #appt_status = 'in_progress',
                    visit_definition=visit_definition,
                    visit_instance=visit_instance)

                if ScheduledEntryBucket.objects.filter(appointment=appointment, entry_status='NEW').exists():
                    self.cleaned_data['appt_status'] = 'incomplete'
        elif appt_status == 'new':
            # must be future relative to best_appt_datetime
            #if t1.days < 0:
            #    raise forms.ValidationError("Status is 'new' so the appointment date must be a future date. You wrote '%s'" % appt_datetime)
            # for new appointments, no matter what, appt_datetime must be greater than
            # any existing appointment for this subject and visit code
            #aggr = Appointment.objects.filter(
            #    registered_subject=registered_subject,
            #    visit_definition__code=visit_definition.code).aggregate(Max('appt_datetime'))
            #if aggr['appt_datetime__max'] != None:
            #    t1 = aggr['appt_datetime__max'] - appt_datetime
            #    if t1.days >= 0:
            #        raise forms.ValidationError("A NEW appointment with appointment date greater than or equal to this date already exists'. You wrote '%s'" % appt_datetime)
            pass
        elif appt_status == 'in_progress':
            # check if any other appointments in progress for this registered_subject
            if Appointment.objects.filter(registered_subject=registered_subject, appt_status='in_progress').exclude(visit_definition__code=visit_definition.code, visit_instance=visit_instance):
                appointments = Appointment.objects.filter(registered_subject=registered_subject, appt_status='in_progress').exclude(visit_definition__code=visit_definition.code, visit_instance=visit_instance)
                raise forms.ValidationError("Another appointment is 'in progress'. Update appointment %s.%s before changing this scheduled appointment to 'in progress'" % (appointments[0].visit_definition.code, appointments[0].visit_instance))
        else:
            raise TypeError("Unknown appt_status passed to clean method in form AppointmentForm. Got %s" % appt_status)
            #must be future
        
        # Always return the full collection of cleaned data.
        return cleaned_data
