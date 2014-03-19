from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.choices.common import YES_NO, GENDER, YES_NO_DWTA
from edc.core.crypto_fields.fields import EncryptedFirstnameField
from edc.core.crypto_fields.utils import mask_encrypted
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household.choices import RELATIONS
from apps.bcpp_household.models import HouseholdStructure
from apps.bcpp_household.models import Plot

from ..choices import (HOUSEHOLD_MEMBER_HTC_PARTICIPATION,
                       HOUSEHOLD_MEMBER_NOT_ELIGIBLE,
                       HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION,
                       HOUSEHOLD_MEMBER_RBD_PARTICIPATION,
                       HOUSEHOLD_MEMBER_FULL_PARTICIPATION,
                       HOUSEHOLD_MEMBER_REFUSED)
from ..managers import HouseholdMemberManager


class HouseholdMember(BaseDispatchSyncUuidModel):

    household_structure = models.ForeignKey(HouseholdStructure,
        null=True,
        blank=False)

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, editable=False)  # will always be set in post_save()

    internal_identifier = models.CharField(
        max_length=36,
        null=True,  # will always be set in post_save()m
        default=None,
        editable=False,
        help_text=('Identifier to track member between surveys, '
                   'is the id of the member\'s first appearance in the table.'))

    first_name = EncryptedFirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[a-zA-Z]{1,250}$", "Ensure first name does not contain any spaces or numbers")],
        db_index=True)

    initials = models.CharField('Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Za-z]{1,3}$", "Must be 2 or 3 letters. No spaces or numbers allowed.")],
        db_index=True)

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER,
        db_index=True)

    age_in_years = models.IntegerField(
        verbose_name='Age in years',
        help_text="If age is unknown, enter 0. If member is less than one year old, enter 1",
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        db_index=True,
        null=True,
        blank=False)

    present_today = models.CharField(
        verbose_name='Is the member present today?',
        max_length=3,
        choices=YES_NO,
        db_index=True)

    member_status = models.CharField(
        max_length=25,
        choices=HOUSEHOLD_MEMBER_FULL_PARTICIPATION,
        null=True,
        editable=False,
        default='NOT_REPORTED',
        help_text='RESEARCH, ABSENT, REFUSED, UNDECIDED',
        db_index=True)

#     member_status = models.CharField(
#         max_length=25,
#         choices=HOUSEHOLD_MEMBER_FULL_PARTICIPATION,
#         null=True,
#         editable=False,
#         default='NOT_REPORTED',
#         help_text='RESEARCH, ABSENT, REFUSED, MOVED',
#         db_index=True)
# 
#     member_status_partial = models.CharField(
#         max_length=25,
#         choices=HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION,
#         null=True,
#         editable=False,
#         default='NOT_REPORTED',
#         help_text='RBD, HTC or RBC/HTC',
#         db_index=True)

    hiv_history = models.CharField(max_length=25, null=True, editable=False)

    eligible_member = models.NullBooleanField(default=None, editable=False, help_text='just based on what is on this form...')

    eligible_subject = models.NullBooleanField(default=None, editable=False, help_text="updated by the bhs eligibility checklist if completed")

    eligible_htc = models.NullBooleanField(default=None, editable=False, help_text="")

    eligible_hoh = models.NullBooleanField(default=None, editable=False, help_text="updated by the head of household eligibility checklist.")

    eligibility_checklist_filled = models.NullBooleanField(default=None, editable=False)

    is_consented = models.BooleanField(default=False, editable=False, help_text="updated in subject consent save method")

    visit_attempts = models.IntegerField(default=0, help_text="")  # TODO: attempts of what? I see visit_attempts on HH HHS and HHM

    target = models.IntegerField(default=0)

    relation = models.CharField(
        verbose_name="Relation to head of household",
        max_length=35,
        choices=RELATIONS,
        null=True,
        help_text="Relation to head of household")

    study_resident = models.CharField(
        verbose_name=("In the past 12 months, have you typically spent 3 or "
                      "more nights per month in this community? "),
        max_length=17,
        choices=YES_NO_DWTA,
        help_text=("If participant has moved into the "
                  "community in the past 12 months, then "
                  "since moving in has the participant typically "
                  "spent 3 or more nights per month in this community."),
        )

    objects = HouseholdMemberManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{0} {1} {2}{3}'.format(
            mask_encrypted(self.first_name),
            self.initials,
            self.age_in_years,
            self.gender)

    def save(self, *args, **kwargs):
        self.eligible_member = (self.is_minor or self.is_adult) and self.study_resident == 'Yes'
        if not self.eligible_member:
            #else it will remain as not reported
            self.member_status = 'NOT_ELIGIBLE'
        self.initials = self.initials.upper()
        self.match_eligibility_values()
        if not self.household_structure.household.enumerated:
            self.household_structure.household.enumerated=True
            self.household_structure.household.save()
        if self.household_structure.enrolled:
            self.eligible_htc = (self.age_in_years >= 16 and not self.is_consented)
        #The following has to be last statement in this save method, after everything else has been updated.
        self.calculate_member_status()
        super(HouseholdMember, self).save(*args, **kwargs)

    def update_plot_eligible_members(self):
        self.household_structure.household.plot.eligible_members = self.__class__.objects.filter(
                                    household_structure__household__plot__plot_identifier=self.household_structure.household.plot.plot_identifier, eligible_member=True).count()
        self.household_structure.household.plot.save()

    def match_eligibility_values(self, exception_cls=None):
        from .enrolment_checklist import EnrolmentChecklist
        validation_error = None
        exception_cls = exception_cls or ValidationError
        #Ensure age is not changed after making HoH
        # TODO: why are you querying HouseholdHeadEligibility???
        if self.eligible_hoh and self.age_in_years < 18:
            validation_error = 'This household member is the head of house. You cannot change their age to less than 18. Got {0}.'.format(self.age_in_years)
        if validation_error:
            raise exception_cls(validation_error)
        #Ensure values used are not changed after capturing enrollment_checklist
        enrollment_checklist = EnrolmentChecklist.objects.filter(household_member=self)
        if enrollment_checklist.exists():
            enrollment_checklist[0].matches_household_member_values(self.age_in_years)

    def natural_key(self):
        if not self.household_structure:
            raise AttributeError("member.household_structure cannot be None for id='\{0}\'".format(self.id))
        if not self.registered_subject:
            raise AttributeError("member.registered_subject cannot be None for id='\{0}\'".format(self.id))
        return self.household_structure.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['bcpp_household.householdstructure', 'registration.registeredsubject']

    @property
    def survey(self):
        return self.household_structure.survey

    @property
    def is_minor(self):
        return (self.age_in_years >= 16 and self.age_in_years <= 17)

    @property
    def is_adult(self):
        return (self.age_in_years >= 18 and self.age_in_years <= 64)

    @property
    def is_htc_only(self):
        """Returns True if subject has participated by accepting HTC only."""
        pass

    def calculate_member_status(self, exception_cls=None):
        """Updates the full participation status.

        .. note:: if the member is consented, no changes are made."""
        #Do not manipulate 'self.eligible_subject' here, it can only be done in the enrollment checklist.
        exception_cls = exception_cls or ValidationError
        SubjectAbsentee = models.get_model('bcpp_household_member', 'SubjectAbsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'SubjectAbsenteeEntry')
        SubjectRefusal = models.get_model('bcpp_household_member', 'SubjectRefusal')
        SubjectUndecided = models.get_model('bcpp_household_member', 'SubjectUndecided')
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'SubjectUndecidedEntry')
        if not self.is_consented:
            #Next two if blocks are for house keeping
            if self.id:
                old_instance = self.__class__.objects.get(pk=self.pk)
            else:
                old_instance = None
            if old_instance and old_instance.member_status != 'ABSENT' and self.member_status != 'ABSENT':
                #Currently not ABSENT, and selected status is also not ABSENT, then delete a SubjectAbsentee without any entries
                if not SubjectAbsenteeEntry.objects.filter(subject_absentee__household_member=self).exists():
                    SubjectAbsentee.objects.filter(household_member=self).delete()
            if old_instance and old_instance.member_status != 'UNDECIDED' and self.member_status != 'UNDECIDED':
                #Currently not UNDECIDED, and selected status is also not UNDECIDED, then delete a SubjectUndecided without any entries
                if not SubjectUndecidedEntry.objects.filter(subject_undecided__household_member=self).exists():
                    SubjectUndecided.objects.filter(household_member=self).delete()
            #Next set of if blocks is for determining allowed status transitions
            if not old_instance and self.member_status not in ['NOT_ELIGIBLE', 'NOT_REPORTED']:
                raise exception_cls('A newly created member can either be NOT_ELIGIBLE or NOT_REPORTED only. Got \'{0}\''.format(self.member_status))
            if old_instance and not old_instance.visit_attempts <= 3:
                #Allowed to change to member status only if visit attempts are less than 3.
                raise exception_cls('Invalid member status change. Visit attempts not less than 3. Got {0}'.format(old_instance.visit_attempts))
            elif self.member_status == 'NOT_REPORTED' and (SubjectAbsentee.objects.filter(household_member=self).exists() or
                SubjectRefusal.objects.filter(household_member=self).exists() or
                SubjectUndecided.objects.filter(household_member=self).exists()):
                #You can only change to NOT_REPORTED if no reports have been captured against subject
                    raise exception_cls('Cannot change member status to NOT_REPORTED. Already reported as either REFUSAL, ABSENTEE or UNDECIDED')
            elif self.member_status == 'NOT_ELIGIBLE' and (self.eligible_member or self.eligible_subject):
                raise exception_cls('This subject passed BHS eligibility or is a BHS potential. Cannot change them to NOT_ELIGIBLE')
            elif old_instance and old_instance.member_status == 'REFUSED' and self.member_status not in ['RESEARCH', 'HTC']:
                raise exception_cls('A refusal can only be changed to either BHS or HTC. Got \'{0}\''.format(self.member_status))
            elif old_instance and old_instance.member_status != 'RESEARCH' and self.member_status == 'RESEARCH':
                #We allow change from any status to 'RESEARCH' for as long as there is no consent.
                self.member_status = 'RESEARCH'
            else:
                pass
        else:
            #Subject is consented and nothing should change.
            pass
        return self.member_status

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def update_hiv_history_on_pre_save(self, **kwargs):
        """Updates from lab_tracker."""
        self.hiv_history = self.get_hiv_history()

    def update_household_member_count_on_post_save(self, sender, using=None):
        """Updates the member count on the household_structure model."""
        household_members = sender.objects.using(using).filter(household_structure=self.household_structure)
        self.household_structure.member_count = household_members.count()
        self.household_structure.enrolled_member_count = len([household_member for household_member in household_members if household_member.is_consented])
        self.household_structure.save(using=using)
        self.update_plot_eligible_members()

    def update_registered_subject_on_post_save(self, **kwargs):
        using = kwargs.get('using', None)
        if not self.internal_identifier:
            self.internal_identifier = self.id
            # decide now, either access an existing registered_subject or create a new one
            if RegisteredSubject.objects.using(using).filter(registration_identifier=self.internal_identifier).exists():
                registered_subject = RegisteredSubject.objects.using(using).get(registration_identifier=self.internal_identifier)
            else:
                # define registered_subject now as the audit trail requires access to the registered_subject object
                # even if no subject_identifier exists. That is, it is going to call
                # get_subject_identifier().
                registered_subject = RegisteredSubject.objects.using(using).create(
                    created=self.created,
                    first_name=self.first_name,
                    initials=self.initials,
                    gender=self.gender,
                    subject_type='subject',
                    registration_identifier=self.internal_identifier,
                    registration_datetime=self.created,
                    user_created=self.user_created,
                    registration_status='member',)
            # set registered_subject for this hsm
            self.registered_subject = registered_subject
            self.save(using=using)

    def get_registered_subject(self):
        return self.registered_subject

    @property
    def is_moved(self):
        from ..models import SubjectMoved
        retval = False
        if SubjectMoved.objects.filter(household_member=self, survey=self.survey):
            retval = True
        return retval

    @property
    def member_status_dashboard(self):
        if self.member_status != 'HTC':
            return self.member_status
        return 'NOT_ELIGIBLE'

    @property
    def status_choices_full(self):
        """"Returns all choices for bhs participation if an eligible member ."""
        status_choices = HOUSEHOLD_MEMBER_FULL_PARTICIPATION
        if not self.eligible_member:
            status_choices = HOUSEHOLD_MEMBER_NOT_ELIGIBLE
        elif self.member_status == 'REFUSED':
            status_choices = HOUSEHOLD_MEMBER_REFUSED
        return status_choices

    @property
    def status_choices_partial(self):
        status_choices = HOUSEHOLD_MEMBER_FULL_PARTICIPATION
        if self.non_bhs_member and self.household_structure.household.enrolled:
            status_choices = HOUSEHOLD_MEMBER_HTC_PARTICIPATION
        elif self.member_status == 'REFUSED':
            enrolled = self.household_structure.number_enrolled
            if enrolled > 0:
                status_choices = HOUSEHOLD_MEMBER_PARTIAL_PARTICIPATION
            elif enrolled == 0:
                status_choices = HOUSEHOLD_MEMBER_RBD_PARTICIPATION
        return status_choices

    @property
    def status_choices_htc(self):
        status_choices = HOUSEHOLD_MEMBER_HTC_PARTICIPATION
        return status_choices

    def _get_form_url(self, model, model_pk=None, add_url=None):
        #SubjectAbsentee would be called with model_pk=None whereas SubjectAbsenteeEntry would be called with model_pk=UUID
        url = ''
        pk = None
        app_label = 'bcpp_household_member'
        if add_url:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
            return url
        if not self.registered_subject:
            self.save()
        if not model_pk:  # This is a like a SubjectAbsentee
            model_class = models.get_model(app_label, model)
            try:
                instance = model_class.objects.get(household_member=self)
                pk = instance.id
            except:
                pk = None
        else:
            pk = model_pk
        if pk:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(pk, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    @property
    def subject_absentee(self):
        """Returns the subject absentee instance for this member and creates a subject_absentee if it does not exist."""
        from ..models import SubjectAbsentee
        return self.entry_instance_factory(SubjectAbsentee, 'ABSENT')

    @property
    def subject_undecided(self):
        """Returns the subject undecided instance for this member and creates a subject_undecided if it does not exist."""
        from ..models import SubjectUndecided
        return self.entry_instance_factory(SubjectUndecided, 'UNDECIDED')

    def entry_instance_factory(self, entry_parent_model, member_status):
        instance = None
        try:
            instance = entry_parent_model.objects.get(household_member=self)
        except entry_parent_model.DoesNotExist:
            if self.member_status == member_status:
                instance = entry_parent_model.objects.create(
                    report_datetime=datetime.today(),
                    registered_subject=self.registered_subject,
                    household_member=self,
                    survey=self.household_structure.survey,
                    )
        return instance

    def render_absentee_info(self):
        """Renders the absentee information for the template."""
        # TODO: model subject absentee should be moved to module bcpp_household_member
        from ..models import SubjectAbsenteeEntry
        render = ['<A href="{0}">add another absentee log entry</A>']
        for subject_absentee_entry, index in enumerate(SubjectAbsenteeEntry(subject_absentee=self.subject_absentee)):
            url = reverse('admin:bcpp_subject_subjectabsenteeenty_change')
            render.update('<A href="{0}">{1}</A>'.format(url, subject_absentee_entry))
        if index < 3:  # not allowed more than three subject absentee entries
            url = reverse('admin:bcpp_subject_subjectabsenteeenty_add')
            render.append('<A href="{0}">add another absentee log entry</A>').format(url)

    @property
    def absentee_form_url(self):
        """Returns a url to the subjectabsentee if an instance exists."""
        return self._get_form_url('subjectabsentee')

    @property
    def absentee_entry_form_urls(self):
        """Returns a url or urls to the subjectabsenteeentry(s) if an instance(s) exists."""
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'subjectabsenteeentry')
        absentee_entry_urls = {}
        subject_absentee = self.subject_absentee
        for entry in SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee).order_by('report_datetime'):
            absentee_entry_urls[entry.pk] = self._get_form_url('subjectabsenteeentry', entry.pk)
        add_url_2 = self._get_form_url('subjectabsenteeentry', model_pk=None, add_url=True)
        absentee_entry_urls['add new entry'] = add_url_2
        return absentee_entry_urls

    def absentee_form_label(self):
        SubjectAbsentee = models.get_model('bcpp_household_member', 'subjectabsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'subjectabsenteeentry')
        return self.form_label_helper(SubjectAbsentee, SubjectAbsenteeEntry)
    absentee_form_label.allow_tags = True

    @property
    def undecided_entry_form_urls(self):
        """Returns a url or urls to the subjectundecidedentry(s) if an instance(s) exists."""
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'subjectundecidedentry')
        undecided_entry_urls = {}
        subject_undecided = self.subject_undecided
        for entry in SubjectUndecidedEntry.objects.filter(subject_undecided=subject_undecided).order_by('report_datetime'):
            undecided_entry_urls[entry.pk] = self._get_form_url('subjectundecidedentry', entry.pk)
        add_url_2 = self._get_form_url('subjectundecidedentry', model_pk=None, add_url=True)
        undecided_entry_urls['add new entry'] = add_url_2
        return undecided_entry_urls

    def undecided_form_label(self):
        SubjectUndecided = models.get_model('bcpp_household_member', 'subjectundecided')
        SubjectUndecidedEntry = models.get_model('bcpp_household_member', 'subjectundecidedentry')
        return self.form_label_helper(SubjectUndecided, SubjectUndecidedEntry)
    undecided_form_label.allow_tags = True

    def form_label_helper(self, model, model_entry):
        report_datetime = []
        model_entry_instances = []
        if model.objects.filter(household_member=self).exists():
            model_instance = model.objects.get(household_member=self)
            if model._meta.module_name == 'subjectundecided':
                model_entry_instances = model_entry.objects.filter(subject_undecided=model_instance).order_by('report_datetime')
            elif model._meta.module_name == 'subjectabsentee':
                model_entry_instances = model_entry.objects.filter(subject_absentee=model_instance).order_by('report_datetime')
            model_entry_count = model_entry_instances.count()
            for subject_undecided_entry in model_entry_instances:
                report_datetime.append((subject_undecided_entry.report_datetime.strftime('%Y-%m-%d'), subject_undecided_entry.id))
            if self.visit_attempts < 3:
                report_datetime.append(('add new entry', 'add new entry'))
        if not report_datetime:
            report_datetime.append(('add new entry', 'add new entry'))
        return report_datetime

    @property
    def refused_form_url(self):
        return self._get_form_url('subjectrefusal')

    @property
    def moved_form_url(self):
        return self._get_form_url('subjectmoved')

    def get_form_label(self, model_name):
        model = models.get_model('bcpp_household_member', model_name)
        if model.objects.filter(household_member=self):
            return model.objects.get(household_member=self)
        else:
            return 'Add "{0}" report'.format(model_name)

    def refused_form_label(self):
        return self.get_form_label('SubjectRefusal')
    refused_form_label.allow_tags = True

    def moved_form_label(self):
        return self.get_form_label('SubjectMoved')
    moved_form_label.allow_tags = True

    def to_locator(self):
        retval = ''
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('admin:bcpp_subject_subjectlocator_changelist')
                retval = '<a href="{0}?q={1}">locator</A>'.format(url, self.registered_subject.subject_identifier)
        return retval
    to_locator.allow_tags = True

    def get_subject_identifier(self):
        """ Uses the hsm internal_identifier to locate the subject identifier in
        registered_subject OR return the hsm.id"""
        if RegisteredSubject.objects.filter(registration_identifier=self.internal_identifier):
            registered_subject = RegisteredSubject.objects.get(registration_identifier=self.internal_identifier)
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        else:
            #$ this should not be an option as all hsm's have a registered_subject instance
            subject_identifier = self.id
        return subject_identifier

    def get_hiv_history(self):
        """Updates and returns hiv history using the site_lab_tracker global.
        """
        hiv_history = ''
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                hiv_history = site_lab_tracker.get_history_as_string('HIV', self.registered_subject.subject_identifier, self.registered_subject.subject_type)
        return hiv_history

    def consent(self):

        """ Gets the consent model instance else return None."""
        # determine related consent models
        related_object_names = [related_object.name for related_object in self._meta.get_all_related_objects() if 'consent' in related_object.name and 'audit' not in related_object.name]
        consent_models = [models.get_model(related_object_name.split(':')[0], related_object_name.split(':')[1]) for related_object_name in related_object_names]
        # search models
        consent_instance = None
        for consent_model in consent_models:
            if consent_model.objects.filter(household_member=self):
                consent_instance = consent_model.objects.get(household_member=self.id)
                break
        return consent_instance

    def deserialize_on_duplicate(self):
        """Lets the deserializer know what to do if a duplicate is found, handled, and about to be saved."""
        retval = False
        if (self.present_today.lower() == 'yes' or self.present_today.lower() == 'no'):
            if self.eligible_member and self.member_status:
                retval = True
            elif not self.eligible_member:
                retval = True
            else:
                pass
        return retval

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        if attrname == 'household_structure' and self.registered_subject:
            subject_identifier = self.registered_subject.subject_identifier
            if subject_identifier:
                registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
                if registered_subject:
                    if HouseholdMember.objects.filter(id=registered_subject.registration_identifier).exists():
                        retval = HouseholdMember.objects.get(id=registered_subject.registration_identifier).household_structure
        return retval

    class Meta:
        ordering = ['-created']
        unique_together = (("household_structure", "first_name", "initials"), ('registered_subject', 'household_structure'))
        app_label = 'bcpp_household_member'
