import re

from django.db import models

from edc.core.identifier.exceptions import IdentifierError
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject
from edc_consent.models import BaseConsent
from edc.device.sync.models import BaseSyncUuidModel

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey


class BaseHouseholdMemberConsent(BaseAppointmentMixin, BaseConsent, BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember, help_text='')

    is_signed = models.BooleanField(default=False)

    survey = models.ForeignKey(Survey, editable=False)  # this updates from household_member in save()

    registered_subject = models.ForeignKey(
        RegisteredSubject,  # this also updates from household_member in save()
        editable=False,
        null=True,
        help_text='one registered subject will be related to one household member for each survey')

    def __unicode__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey = self.household_member.household_structure.survey
            self.registered_subject = self.household_member.registered_subject
        super(BaseHouseholdMemberConsent, self).save(*args, **kwargs)

    def _check_if_duplicate_subject_identifier(self, using):
        """Checks if the subject identifier is in use, for new and existing instances.

        .. warning:: this overrides default behavior!

        .. note:: overriding to change the constraint to subject_identifier + survey
                  instead of just subject_identifier."""
        if not self.pk and self.subject_identifier:
            if self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey):
                obj = self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey)
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} and survey {2} when '
                                      'saving {1} on add. See {3}.'.format(
                                          self.subject_identifier, self, self.survey, obj))
        else:
            if self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey).exclude(pk=self.pk):
                obj = self.__class__.objects.using(using).filter(
                    subject_identifier=self.subject_identifier, survey=self.survey).exclude(pk=self.pk)
                raise IdentifierError('Attempt to insert duplicate value for '
                                      'subject_identifier {0} and survey {2} when '
                                      'saving {1} on change. See {3}.'.format(
                                          self.subject_identifier, self, self.survey, obj))
        self.check_for_duplicate_subject_identifier()

    def check_for_duplicate_subject_identifier(self):
        """Users may override to add an additional strategy to detect duplicate identifiers."""
        pass

    def post_save_update_registered_subject(self, using, **kwargs):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if re_pk.match(self.registered_subject.subject_identifier):
            self.registered_subject.subject_identifier = self.subject_identifier
        self.registered_subject.registration_status = 'CONSENTED'
        self.registered_subject.save(using=using)
        if self.subject_identifier != self.registered_subject.subject_identifier:
            raise TypeError('Subject identifier expected to be same as registered_subject '
                            'subject_identifier. Got {0} != {1}'.format(
                                self.subject_identifier, self.registered_subject.subject_identifier))

    def dispatch_container_lookup(self, using=None):
        return (('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    def deserialize_get_missing_fk(self, attrname):
        if attrname == 'household_member':
            registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
            survey = self.survey
            internal_identifier = registered_subject.registration_identifier
            household_member = self.household_member.__class__.objects.get(
                internal_identifier=internal_identifier,
                survey=survey)
            retval = household_member
        else:
            retval = None
        return retval

    class Meta:
        abstract = True
