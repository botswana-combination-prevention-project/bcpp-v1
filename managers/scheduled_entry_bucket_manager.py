from django.db.models import get_model
from bhp_entry.managers import BaseEntryBucketManager
from bhp_content_type_map.models import ContentTypeMap
from bhp_registration.models import RegisteredSubject
from bhp_visit.models import VisitDefinition
from bhp_appointment.models import Appointment


class ScheduledEntryBucketManager(BaseEntryBucketManager):
    def get_by_natural_key(self, visit_instance, code, identity, first_name, dob, initials, registration_identifier, visit_definition, app_label, model):
        registered_subject = RegisteredSubject.objects.get(
            identity=identity,
            first_name=first_name,
            dob=dob,
            initials=initials,
            registration_identifier=registration_identifier
            )

        visit_definition = VisitDefinition.objects.get(code=code)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition=visit_definition,
            visit_instance=visit_instance
            )
        content_map_type = ContentTypeMap.objects.get(
            app_label=app_label,
            model=model
            )
        model = get_model('bhp_entry', 'Entry')
        entry = model.objects.get(
            content_map_type=content_map_type,
            visit_definition=visit_definition
            )
        return self.get(
            entry=entry,
            appointment=appointment
            )

#
#    def is_keyed(self, model=None, fk_fieldname_to_visit_model=None):
#        """ Confirms if model instance exists / is_keyed """
#        if not model:
#            model = self.entry.content_type_map.model_class()
#        if not fk_fieldname_to_visit_model:
#            visit_model_helper = VisitModelHelper()
#            fk_fieldname_to_visit_model = visit_model_helper.get_visit_field(model=model, visit_model=self.visit_model_instance)
#            if not fk_fieldname_to_visit_model:
#                raise AttributeError('Attribute \'visit_fk_name\' is required for method is_keyed in %s' % (self,))
#        try:
#            is_keyed = model.objects.filter(**{fk_fieldname_to_visit_model: self.visit_model_instance}).exists()
#        except FieldError as e:
#            raise ImproperlyConfigured('{0}. Perhaps a model is included in the visit definition that does not belong or '
#                                               'you need to update your content_type_map. '
#                                               'Got entry for "{1}" in visit_definition {2}'.format(e, self.entry, getattr(model, fk_fieldname_to_visit_model).appointment.visit_definition))
#        return is_keyed
#
#    def get_entries_for(self, **kwargs):
#        """Returns a list of ScheduledEntryBucket instance for the given subject and appointment.
#
#        Note that ScheduledEntryBucket objects are linked to a subject's appointment
#        for visit_instance = '0'; that is, the first appointment for
#        a timepoint/visit.
#        """
#        entry_category = kwargs.get("entry_category", 'clinic')
#        registered_subject = kwargs.get("registered_subject")
#        if not registered_subject:
#            raise TypeError("Manager get_schedule_forms_for expected registered_subject. Got None.")
#        appt_0 = kwargs.get("appointment")
#        scheduled_entry_bucket_list = []
#        if appt_0:
#            # get the scheduled crfs based on the appt for visit_instance = '0'
#            for  scheduled_entry_bucket in super(ScheduledEntryBucketManager, self).values('pk').filter(
#                                                registered_subject_id=registered_subject.pk,
#                                                appointment_id=appt_0.pk,
#                                                entry__entry_category=entry_category,
#                                                ).order_by('entry__entry_order'):
#                scheduled_entry_bucket_list.append(super(ScheduledEntryBucketManager, self).select_related().get(pk=scheduled_entry_bucket.get('pk')))
#        return scheduled_entry_bucket_list
#
#    def add_or_update_for_visit(self, visit_model_instance):
#        """ Adds entries or updates existing entries to the scheduled_entry_bucket for a given visit_model."""
#        try:
#            registered_subject = visit_model_instance.appointment.registered_subject
#        except FieldError:
#            raise AttributeError("ScheduledEntryBucketManager expects model {0} to have attribute \'appointment\'.".format(visit_model_instance._meta.object_name))
#        # scheduled entries are only added if visit instance is 0
#        if visit_model_instance.appointment.visit_instance == '0':
#            filled_datetime = datetime.today()
#            report_datetime = visit_model_instance.report_datetime
#            # fetch entries required for this the visit definition of this visit_model_instance.appointment
#            visit_model_helper = VisitModelHelper()
#            fk_fieldname_to_visit_model = None
#            for entry in Entry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition):
#                # TODO: calculate due date -- "needs work"
#                due_datetime = entry.visit_definition.get_upper_window_datetime(report_datetime)
#                model = entry.content_type_map.model_class()
#                entry_status = 'NEW'
#                # check if entry.entry_form.model has been keyed for this registered_subject, timepoint
#                # if so, set report date and status accordingly
#                # scheduled forms have a foreign key to a visit_model_instance
#                if not fk_fieldname_to_visit_model:
#                    fk_fieldname_to_visit_model = visit_model_helper.get_visit_field(model=model, visit_model=visit_model_instance)
#                if self.is_keyed(model, fk_fieldname_to_visit_model):
#                    report_datetime = visit_model_instance.report_datetime
#                    entry_status = 'KEYED'
#                options = {'current_entry_title': model._meta.verbose_name,
#                           'fill_datetime': filled_datetime,
#                           'due_datetime': due_datetime,
#                           'report_datetime': None,
#                           'entry_status': entry_status}
#                scheduled_entry_bucket, created = super(ScheduledEntryBucketManager, self).get_or_create(
#                        registered_subject=registered_subject,
#                        appointment=visit_model_instance.appointment,
#                        entry=entry,
#                        defaults=options)
#                if not created:
#                    scheduled_entry_bucket.report_datetime = report_datetime
#                    if scheduled_entry_bucket.entry_status == 'NEW':
#                        scheduled_entry_bucket.entry_status = entry_status
#                    scheduled_entry_bucket.save()
#
#    def update_status(self, model, visit_model_instance, action, comment=None):
#
#        """Updates bucket status, etc for a given entry in bucket.
#        usually called from bucket controller.
#        """
#        action_terms = ['new', 'keyed', 'not_required', 'delete']
#        if action not in action_terms:
#            raise ValueError('Action must be %s. Got %s' % (action_terms, action))
#        # try to update
#        # if self.entry is None implies Entry has no occurrence for this visit_definition, content_type_map,
#        # which is OK.
#        # see method set_entry()
#        if Entry.objects.filter(visit_definition=visit_model_instance.appointment.visit_definition).exists():
#            entry = Entry.objects.get(visit_definition=visit_model_instance.appointment.visit_definition)
#            if visit_model_instance:
#                if super(ScheduledEntryBucketManager, self).filter(registered_subject=self.registered_subject,
#                                                                   appointment=self.appointment,
#                                                                   entry=entry).exists():
#                    # already in bucket, so get bucket entry
#                    scheduled_entry_bucket = super(ScheduledEntryBucketManager, self).get(registered_subject=self.registered_subject,
#                                                                                          appointment=self.appointment,
#                                                                                          entry=entry)
#                    # update entry_status if NEW no matter what, to indictate perhaps that it was modified
#                    status = self.get_status(
#                        action=action,
#                        report_datetime=self.report_datetime,
#                        current_status=scheduled_entry_bucket.entry_status,
#                        entry_comment=comment)
#                    scheduled_entry_bucket.report_datetime = status['report_datetime']
#                    scheduled_entry_bucket.entry_status = status['action']
#                    scheduled_entry_bucket.entry_comment = status['entry_comment']
#                    scheduled_entry_bucket.close_datetime = status['close_datetime']
#                    scheduled_entry_bucket.modified = datetime.today()
#                    scheduled_entry_bucket.save()
#                else:
#                    # create a new scheduled bucket entry instance
#                    #
#                    super(ScheduledEntryBucketManager, self).create(
#                        created=datetime.today(),
#                        modified=datetime.today(),
#                        registered_subject=self.registered_subject,
#                        current_entry_title=entry.content_type_map.model.lower(),
#                        entry_status='NEW',
#                        due_datetime=None,
#                        report_datetime=datetime.today(),
#                        entry_comment='auto',
#                        close_datetime=None,
#                        fill_datetime=None,
#                        appointment=self.appointment,
#                        entry=entry)
#            else:
#                raise AttributeError('Cannot determine visit model. See %s update_status()' % (self,))
