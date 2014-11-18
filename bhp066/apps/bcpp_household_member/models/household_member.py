from datetime import date
from dateutil.relativedelta import relativedelta

from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.choices.common import YES_NO, GENDER, YES_NO_DWTA
from edc.core.crypto_fields.fields import EncryptedFirstnameField
from edc.core.crypto_fields.utils import mask_encrypted
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.constants import NOT_APPLICABLE

from apps.bcpp_household.models import HouseholdStructure, RepresentativeEligibility
from apps.bcpp_household.models import Plot
from apps.bcpp_household.exceptions import AlreadyReplaced
from apps.bcpp.choices import INABILITY_TO_PARTICIPATE_REASON

from ..choices import HOUSEHOLD_MEMBER_PARTICIPATION, RELATIONS
from ..classes import HouseholdMemberHelper
from ..constants import ABSENT, UNDECIDED, BHS_SCREEN, REFUSED
from ..exceptions import MemberStatusError
from ..managers import HouseholdMemberManager

from django.conf import settings
from edc.map.classes.controller import site_mappers


class HouseholdMember(BaseDispatchSyncUuidModel):
    """A model completed by the user to represent an enumerated household member."""
    household_structure = models.ForeignKey(HouseholdStructure, null=True, blank=False)

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, editable=False)

    first_name = EncryptedFirstnameField(
        verbose_name='First name',
        validators=[RegexValidator("^[A-Z]{1,250}$",
                                   ("Ensure first name is only CAPS and "
                                    "does not contain any spaces or numbers"))
                    ],
        db_index=True)

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(3),
            RegexValidator("^[A-Z]{1,3}$",
                           ("Must be Only CAPS and 2 or 3 letters. "
                            "No spaces or numbers allowed."))],
        db_index=True)

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER,
        db_index=True)

    age_in_years = models.IntegerField(
        verbose_name=_('Age in years'),
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        db_index=True,
        null=True,
        blank=False,
        help_text=("If age is unknown, enter 0. If member is less "
                   "than one year old, enter 1"),
        )

    present_today = models.CharField(
        verbose_name=_('Is the member present today?'),
        max_length=3,
        choices=YES_NO,
        db_index=True)

    relation = models.CharField(
        verbose_name=_("Relation to head of household"),
        max_length=35,
        choices=RELATIONS,
        null=True,
        help_text="Relation to head of household")

    inability_to_participate = models.CharField(
        verbose_name=_("Do any of the following reasons apply to the participant?"),
        max_length=17,
        choices=INABILITY_TO_PARTICIPATE_REASON,
        help_text=("Participant can only participate if NONE is selected. "
                   "(Any of these reasons make the participant unable to take "
                   "part in the informed consent process)"),
        )

    study_resident = models.CharField(
        verbose_name=_("In the past 12 months, have you typically spent 3 or "
                       "more nights per month in this community? "),
        max_length=17,
        choices=YES_NO_DWTA,
        help_text=("If participant has moved into the "
                   "community in the past 12 months, then "
                   "since moving in has the participant typically "
                   "spent 3 or more nights per month in this community."))

    internal_identifier = models.CharField(
        max_length=36,
        null=True,  # will always be set in post_save()m
        default=None,
        editable=False,
        help_text=_('Identifier to track member between surveys, '
                    'is the id of the member\'s first appearance in the table.'))

    visit_attempts = models.IntegerField(
        default=0,
        editable=False,
        help_text="")

    member_status = models.CharField(
        max_length=25,
        choices=HOUSEHOLD_MEMBER_PARTICIPATION,
        null=True,
        editable=False,
        help_text='RESEARCH, ABSENT, REFUSED, UNDECIDED',
        db_index=True)

    hiv_history = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    eligible_member = models.NullBooleanField(
        default=False,
        editable=False,
        help_text='eligible to be screened. based on data on this form')

    eligible_subject = models.NullBooleanField(
        default=False,
        editable=False,
        help_text=('updated by the enrollment checklist save method only. True if subject '
                   'passes the eligibility criteria.'))

    enrollment_checklist_completed = models.NullBooleanField(
        default=False,
        editable=False,
        help_text=('updated by enrollment checklist only (regardless of the '
                   'eligibility outcome).'))

    enrollment_loss_completed = models.NullBooleanField(
        default=False,
        editable=False,
        help_text="updated by enrollment loss save method only.")

    refused = models.BooleanField(
        default=False,
        editable=False,
        help_text="updated by subject refusal save method only")

    undecided = models.BooleanField(
        default=False,
        editable=False,
        help_text="updated by subject undecided save method only")

    refused_htc = models.BooleanField(
        default=False,
        editable=False,
        help_text="updated by subject HTC save method only")

    htc = models.BooleanField(
        default=False,
        editable=False,
        help_text="updated by the subject HTC save method only")

    is_consented = models.BooleanField(
        default=False,
        editable=False, help_text="updated by the subject consent save method only")

    eligible_htc = models.NullBooleanField(
        default=False,
        editable=False,
        help_text="")

    eligible_hoh = models.NullBooleanField(
        default=False,
        editable=False,
        help_text="updated by the head of household enrollment checklist only.")

    reported = models.BooleanField(
        default=False,
        editable=False,
        help_text="update by any of subject absentee, undecided, refusal")

    absent = models.BooleanField(
        default=False,
        editable=False,
        help_text="Updated by the subject absentee log")

    target = models.IntegerField(
        default=0,
        editable=False,
        )

    objects = HouseholdMemberManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{0} {1} {2}{3} {4}'.format(
            mask_encrypted(self.first_name),
            self.initials,
            self.age_in_years,
            self.gender,
            '' if self.is_bhs else 'non-BHS')

    def save(self, *args, **kwargs):
        selected_member_status = None
        using = kwargs.get('using')
        self.allow_enrollment(using)
        self.check_eligible_representative_filled(self.household_structure, using=using)
        if self.household_structure.household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(
                self.household_structure.household.household_identifier))
        # check if consented. If update fields is set then bypass (see SubjectConsent post-save signal)
        if self.is_consented and not kwargs.get('update_fields'):
            raise MemberStatusError('Household member is consented. Changes are not allowed. '
                                    'Perhaps catch this in the form.')
        self.eligible_member = self.is_eligible_member
        self.absent = True if (not self.id and self.present_today == 'No') else self.absent
        if kwargs.get('update_fields') == ['member_status']:  # when updated by participation view
            selected_member_status = self.member_status
            if self.member_status == BHS_SCREEN:
                self.undecided = False
                self.absent = False
                self.eligible_htc = False
                if self.refused:
                    self.clear_refusal
                if self.enrollment_checklist_completed:
                    self.clear_enrollment_checklist
                if self.htc:
                    self.clear_htc
            if self.member_status == REFUSED:
                if self.enrollment_checklist_completed:
                    self.clear_enrollment_checklist
            else:
                self.undecided = True if selected_member_status == UNDECIDED else False
                self.absent = True if selected_member_status == ABSENT else False
        if self.intervention and self.plot_enrolled:
            self.eligible_htc = self.evaluate_htc_eligibility
        elif not self.intervention:
            self.eligible_htc = self.evaluate_htc_eligibility
        household_member_helper = HouseholdMemberHelper(self)
        self.member_status = household_member_helper.member_status(selected_member_status)
        try:
            update_fields = kwargs.get('update_fields') + [
                'member_status', 'undecided', 'absent', 'refused', 'eligible_member', 'eligible_htc',
                'enrollment_checklist_completed', 'enrollment_loss_completed', 'htc']
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(HouseholdMember, self).save(*args, **kwargs)

    def allow_enrollment(self, using, exception_cls=None, instance=None):
        """Raises an exception if the household is not enrolled
        and BHS_FULL_ENROLLMENT_DATE is past."""
        instance = instance or self
        return self.household_structure.household.plot.allow_enrollment(
            using, exception_cls=exception_cls,
            plot_instance=instance.household_structure.household.plot)

    @property
    def clear_refusal(self):
        from ..models import SubjectRefusal
        self.refused = False
        try:
            SubjectRefusal.objects.get(household_member=self).delete()
        except SubjectRefusal.DoesNotExist:
            pass

    @property
    def clear_htc(self):
        from ..models import SubjectHtc
        self.htc = False
        self.eligible_htc = False
        try:
            SubjectHtc.objects.get(household_member=self).delete()
        except SubjectHtc.DoesNotExist:
            pass

    @property
    def clear_enrollment_checklist(self):
        from ..models import EnrollmentChecklist
        self.enrollment_checklist_completed = False
        self.enrollment_loss_completed = False
        self.eligible_subject = False
        try:
            EnrollmentChecklist.objects.get(household_member=self).delete()
        except EnrollmentChecklist.DoesNotExist:
            pass

    @property
    def evaluate_htc_eligibility(self):
        eligible_htc = False
        if self.age_in_years > 64:
            eligible_htc = True
        elif ((not self.eligible_member and self.inability_to_participate == NOT_APPLICABLE) and
              self.age_in_years >= 16):
            eligible_htc = True
        elif self.eligible_member and self.refused:
            eligible_htc = True
        elif self.enrollment_checklist_completed and not self.eligible_subject:
            eligible_htc = True
        return eligible_htc

    @property
    def intervention(self):
        return site_mappers.get_current_mapper().intervention

    @property
    def plot_enrolled(self):
        return self.household_structure.household.plot.bhs

    @property
    def is_eligible_member(self):
        return (self.age_in_years >= 16 and self.age_in_years <= 64 and self.study_resident == 'Yes'
                and self.inability_to_participate == NOT_APPLICABLE)

    def check_eligible_representative_filled(self, household_structure, using=None, exception_cls=None):
        """Raises an exception if the RepresentativeEligibility form has not been completed.

        Without RepresentativeEligibility, a HouseholdMember cannot be added."""
        exception_cls = exception_cls or ValidationError
        using = using or 'default'
        try:
            RepresentativeEligibility.objects.using(using).get(household_structure=household_structure)
        except RepresentativeEligibility.DoesNotExist:
            raise exception_cls('The Eligibility Checklist for an eligible '
                                'representative has not been completed.')

    def check_head_household(self, household_structure, using=None, exception_cls=None):
        """Raises an exception if the HeadOusehold already exists in this household structure."""
        exception_cls = exception_cls or ValidationError
        using = using or 'default'
        try:
            current_hoh = HouseholdMember.objects.get(
                    household_structure=household_structure,
                    relation='Head')
            # If i am not a new instance then make sure i am not comparing to myself.
            if self.id and current_hoh and (self.id != current_hoh.id):
                    raise exception_cls('{0} is the head of household already. Only one member '
                                                'may be the head of household.'.format(current_hoh))
            # If i am a new instance then i could not be comparing to myself as i do not exist in the DB yet
            elif not self.id and current_hoh:
                raise exception_cls('{0} is the head of household already. Only one member '
                                                'may be the head of household.'.format(current_hoh))
        except HouseholdMember.DoesNotExist:
            pass

    def match_enrollment_checklist_values(self, household_member, exception_cls=None):
        if household_member.enrollment_checklist:
            household_member.enrollment_checklist.matches_household_member_values(
                household_member.enrollment_checklist, household_member, exception_cls)

    @property
    def enrollment_checklist(self):
        """Returns the enrollment checklist instance or None."""
        EnrollmentChecklist = models.get_model('bcpp_household_member', 'EnrollmentChecklist')
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(household_member=self)
        except EnrollmentChecklist.DoesNotExist:
            enrollment_checklist = None
        return enrollment_checklist

    @property
    def subject_htc(self):
        """Returns the SubjectHtc instance or None."""
        SubjectHtc = models.get_model('bcpp_household_member', 'SubjectHtc')
        try:
            subject_htc = SubjectHtc.objects.get(household_member=self)
        except SubjectHtc.DoesNotExist:
            subject_htc = None
        return subject_htc

    @property
    def bypass_household_log(self):
        try:
            return settings.BYPASS_HOUSEHOLD_LOG
        except AttributeError:
            return False

    @property
    def enrollment_options(self):
        """Returns a dictionary of household member fields that are also
        on the enrollment checklist (as a convenience)."""
        return {'gender': self.gender,
                'dob': date.today() - relativedelta(years=self.age_in_years),
                'initials': self.initials,
                'part_time_resident': self.study_resident}

    def natural_key(self):
        if not self.household_structure:
            raise AttributeError("household_member.household_structure cannot "
                                 "be None for id='\{0}\'".format(self.id))
        if not self.registered_subject:
            raise AttributeError("household_member.registered_subject cannot "
                                 "be None for id='\{0}\'".format(self.id))
        return self.household_structure.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['bcpp_household.householdstructure',
                                'registration.registeredsubject']

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

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def update_hiv_history_on_pre_save(self, using, **kwargs):
        """Updates from lab_tracker."""
        self.hiv_history = self.get_hiv_history()

    def update_household_member_count_on_post_save(self, sender, using=None):
        """Updates the member count on the household_structure model."""
        household_members = sender.objects.using(using).filter(
            household_structure=self.household_structure)
        self.household_structure.member_count = household_members.count()
        self.household_structure.enrolled_member_count = len(
            [household_member for household_member in household_members if household_member.is_consented])
        self.household_structure.save(using=using)

    def update_registered_subject_on_post_save(self, using, **kwargs):
        if not self.internal_identifier:
            self.internal_identifier = self.id
            # decide now, either access an existing registered_subject or create a new one
            try:
                registered_subject = RegisteredSubject.objects.using(using).get(
                    registration_identifier=self.internal_identifier)
            except RegisteredSubject.DoesNotExist:
                # define registered_subject now as the audit trail requires access
                # to the registered_subject object even if no subject_identifier
                # exists. That is, it is going to call get_subject_identifier().
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
    def member_status_choices(self):
        return HouseholdMemberHelper(self).member_status_choices

    def _get_form_url(self, model, model_pk=None, add_url=None):
        # SubjectAbsentee would be called with model_pk=None
        # whereas SubjectAbsenteeEntry would be called with model_pk=UUID
        url = ''
        app_label = 'bcpp_household_member'
        if add_url:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
            return url
        elif not model_pk:
            model_class = models.get_model(app_label, model)
            try:
                instance = model_class.objects.get(household_member=self)
                model_pk = instance.id
            except model_class.DoesNotExist:
                model_pk = None
        if model_pk:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model), args=(model_pk, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model))
        return url

    def render_absentee_info(self):
        """Renders the absentee information for the template."""
        from ..models import SubjectAbsenteeEntry
        render = ['<A href="{0}">add another absentee log entry</A>']
        for subject_absentee_entry, index in enumerate(SubjectAbsenteeEntry(
                subject_absentee=self.subject_absentee_instance)):
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
    def subject_absentee_instance(self):
        """Returns the subject absentee instance for this member
        and creates a subject_absentee_instance if it does not exist."""
        SubjectAbsentee = models.get_model('bcpp_household_member', 'subjectabsentee')
        try:
            subject_absentee = SubjectAbsentee.objects.get(household_member__pk=self.pk)
        except SubjectAbsentee.DoesNotExist:
            subject_absentee = ''
        return subject_absentee

    @property
    def subject_undecided_instance(self):
        """Returns the subject undecided instance for this member
        and creates a subject_undecided_instance if it does not exist."""
        SubjectUndecided = models.get_model('bcpp_household_member', 'subjectundecided')
        try:
            subject_undecided = SubjectUndecided.objects.get(household_member__pk=self.pk)
        except SubjectUndecided.DoesNotExist:
            subject_undecided = ''
        return subject_undecided

    @property
    def absentee_entry_form_urls(self):
        """Returns a url or urls to the subjectabsenteeentry(s) if an instance(s) exists.

        Urls are used on the Household Composition dashboard to allow edits of existing
        instances and an option to add one more.

        Format is {pk: }"""
        urls = {}
        app_label = 'bcpp_household_member'
        model = 'subjectabsenteeentry'
        SubjectAbsentee = models.get_model(app_label, 'subjectabsentee')
        SubjectAbsenteeEntry = models.get_model(app_label, model)
        try:
            subject_absentee = SubjectAbsentee.objects.get(household_member=self)
            for subject_absentee_entry in SubjectAbsenteeEntry.objects.filter(
                    subject_absentee=subject_absentee).order_by('report_datetime'):
                # add url for each existing instance
                urls[subject_absentee_entry.pk] = reverse(
                    'admin:{0}_{1}_change'.format(app_label, model),
                    args=(subject_absentee_entry.pk, ))
            # always add an extra add url
            urls['add new entry'] = reverse('admin:{0}_{1}_add'.format(app_label, model))
        except SubjectAbsentee.DoesNotExist:
            pass
        return urls

    @property
    def undecided_entry_form_urls(self):
        """Returns a url or urls to the subject_undecided_entry(s) if an instance(s) exists.

        Urls are used on the Household Composition dashboard to allow edits of existing
        instances and an option to add one more.

        Format is {pk: }"""
        urls = {}
        app_label = 'bcpp_household_member'
        model = 'subjectundecidedentry'
        SubjectUndecided = models.get_model(app_label, 'subjectundecided')
        SubjectUndecidedEntry = models.get_model(app_label, model)
        try:
            subject_undecided = SubjectUndecided.objects.get(household_member=self)
            for subject_undecided_entry in SubjectUndecidedEntry.objects.filter(
                    subject_undecided=subject_undecided).order_by('report_datetime'):
                # add url for each existing instance
                urls[subject_undecided_entry.pk] = reverse(
                    'admin:{0}_{1}_change'.format(app_label, model),
                    args=(subject_undecided_entry.pk, ))
            # always add an extra add url
            urls['add new entry'] = reverse('admin:{0}_{1}_add'.format(app_label, model))
        except SubjectUndecided.DoesNotExist:
            pass
        return urls

    def absentee_form_label(self):
        SubjectAbsentee = models.get_model('bcpp_household_member', 'subjectabsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_household_member', 'subjectabsenteeentry')
        return self.form_label_helper(SubjectAbsentee, SubjectAbsenteeEntry)
    absentee_form_label.allow_tags = True

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
                model_entry_instances = model_entry.objects.filter(
                    subject_undecided=model_instance).order_by('report_datetime')
            elif model._meta.module_name == 'subjectabsentee':
                model_entry_instances = model_entry.objects.filter(
                    subject_absentee=model_instance).order_by('report_datetime')
            for subject_undecided_entry in model_entry_instances:
                report_datetime.append((subject_undecided_entry.report_datetime.strftime('%Y-%m-%d'),
                                        subject_undecided_entry.id))
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
                retval = '<a href="{0}?q={1}">locator</A>'.format(
                    url, self.registered_subject.subject_identifier)
        return retval
    to_locator.allow_tags = True

    def get_subject_identifier(self):
        """ Uses the hsm internal_identifier to locate the subject identifier in
        registered_subject OR return the hsm.id"""
        if RegisteredSubject.objects.filter(registration_identifier=self.internal_identifier):
            registered_subject = RegisteredSubject.objects.get(
                registration_identifier=self.internal_identifier)
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        else:
            # this should not be an option as all hsm's have a registered_subject instance
            subject_identifier = self.id
        return subject_identifier

    def get_hiv_history(self):
        """Updates and returns hiv history using the site_lab_tracker global.
        """
        hiv_history = ''
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                hiv_history = site_lab_tracker.get_history_as_string(
                    'HIV', self.registered_subject.subject_identifier,
                    self.registered_subject.subject_type)
        return hiv_history

    def consent(self):

        """ Gets the consent model instance else return None."""
        # determine related consent models
        related_object_names = [related_object.name
                                for related_object in self._meta.get_all_related_objects()
                                if 'consent' in related_object.name and
                                'audit' not in related_object.name]
        consent_models = [models.get_model(related_object_name.split(':')[0],
                                           related_object_name.split(':')[1])
                          for related_object_name in related_object_names]
        # search models
        consent_instance = None
        for consent_model in consent_models:
            if consent_model.objects.filter(household_member=self):
                consent_instance = consent_model.objects.get(household_member=self.id)
                break
        return consent_instance

    @property
    def is_bhs(self):
        """Returns True if the member was survey as part of the BHS."""
        return self.household_structure.household.plot.plot_identifier != \
            site_mappers.get_current_mapper()().clinic_plot.plot_identifier

    def deserialize_on_duplicate(self):
        """Lets the deserializer know what to do if a duplicate is found,
        handled, and about to be saved."""
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
                        retval = HouseholdMember.objects.get(
                            id=registered_subject.registration_identifier).household_structure
        return retval

    class Meta:
        ordering = ['-created']
        unique_together = (("household_structure", "first_name", "initials"),
                           ('registered_subject', 'household_structure'))
        app_label = 'bcpp_household_member'
        index_together = [['id', 'registered_subject', 'created'], ]
