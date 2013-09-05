from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from django.db.models.signals import Signal, post_save
from audit_trail.audit import AuditTrail
from bhp_crypto.utils import mask_encrypted
from bhp_registration.models import RegisteredSubject
from bhp_household_member.models import BaseHouseholdMember
from bcpp_survey.models import Survey
from bcpp_household.choices import RELATIONS
from bcpp_household.models import Household
from bcpp_household.models import HouseholdStructure
from bcpp_household_member.managers import HouseholdMemberManager

from contact_log import ContactLog


class HouseholdMember(BaseHouseholdMember):

    household_structure = models.ForeignKey(HouseholdStructure,
        null=True,
        blank=True)

    household = models.ForeignKey(Household, null=True, editable=False)

    survey = models.ForeignKey(Survey, editable=False)

    relation = models.CharField(
        verbose_name="Relation to head of household",
        max_length=35,
        choices=RELATIONS,
        null=True,
        help_text="Relation to head of household")

    nights_out = models.IntegerField("Nights spent outside of this community (per month)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(31)],
        db_index=True)

    relation = models.CharField(
        verbose_name="Relation to head of household",
        max_length=35,
        choices=RELATIONS,
        null=True,
        help_text="Relation to head of household")

    contact_log = models.OneToOneField(ContactLog, null=True)

    history = AuditTrail()

    objects = HouseholdMemberManager()

    def natural_key(self):
        if not self.household_structure:
            raise AttributeError("member.household_structure cannot be None for pk='\{0}\'".format(self.pk))
        if not self.registered_subject:
            raise AttributeError("member.registered_subject cannot be None for pk='\{0}\'".format(self.pk))
        return self.household_structure.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['bcpp_household.householdstructure', 'bhp_registration.registeredsubject']

    def __unicode__(self):
        return '{0} of {1} ({2}{3}) {4}'.format(
            mask_encrypted(self.first_name),
            self.household_structure,
            self.age_in_years,
            self.gender,
            self.survey.survey_name)

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household_structure__household__household_identifier')

    def update_hiv_history_on_pre_save(self, **kwargs):
        """Updates from lab_tracker."""
        self.hiv_history = self.get_hiv_history()

    def update_household_member_count_on_post_save(self, **kwargs):
        using = kwargs.get('using', None)
        self.household_structure.member_count = self.__class__.objects.filter(household_structure=self.household_structure).count()
        self.household_structure.save(using=using)

    def update_registered_subject_on_post_save(self, **kwargs):
        using = kwargs.get('using', None)
        if not self.internal_identifier:
            self.internal_identifier = self.pk
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

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if not self.survey_id:
            if self.household_structure:
                self.survey = self.household_structure.survey
            else:
                self.survey = Survey.objects.using(using).get(datetime_start__lte=self.created, datetime_end__gte=self.created)
        if not self.household:
            self.household = self.household_structure.household
        super(HouseholdMember, self).save(*args, **kwargs)

    def deserialize_prep(self):
        Signal.disconnect(post_save, None, weak=False, dispatch_uid="member_on_post_save")

    def deserialize_post(self):
        Signal.connect(post_save, None, weak=False, dispatch_uid="member_on_post_save")

    @property
    def is_moved(self):
        from bcpp_subject.models import SubjectMoved
        retval = False
        if SubjectMoved.objects.filter(household_member=self, survey=self.survey):
            retval = True
        return retval

    @property
    def participation_form(self):
        """Returns a form object for the household survey dashboard."""
        from bcpp_household_member.forms import ParticipationForm
        if not self.member_status:
            self.member_status = 'NOT_REPORTED'
        return ParticipationForm(initial={'status': self.member_status,
                                          'household_member': self.pk,
                                          'dashboard_id': self.pk,
                                          'dashboard_model': 'household_structure',
                                          'dashboard_type': 'household'})

    def _get_form_url(self, model_name):
        url = ''
        pk = None
        app_label = 'bcpp_subject'
        if not self.registered_subject:
            self.save()
        Model = models.get_model(app_label, model_name)
        if Model.objects.filter(household_member=self):
            pk = Model.objects.get(household_member=self).pk
        if pk:
            url = reverse('admin:{0}_{1}_change'.format(app_label, model_name), args=(pk, ))
        else:
            url = reverse('admin:{0}_{1}_add'.format(app_label, model_name))
        return url

    @property
    def absentee_form_url(self):
        """Returns a url to the subjectabsentee if an instance exists."""
        return self._get_form_url('subjectabsentee')

    def absentee_form_label(self):
        SubjectAbsentee = models.get_model('bcpp_subject', 'subjectabsentee')
        SubjectAbsenteeEntry = models.get_model('bcpp_subject', 'subjectabsenteeentry')
        report_datetime = []
        if SubjectAbsentee.objects.filter(household_member=self):
            subject_absentee = SubjectAbsentee.objects.get(household_member=self)
            for subject_absentee_entry in SubjectAbsenteeEntry.objects.filter(subject_absentee=subject_absentee).order_by('report_datetime'):
                report_datetime.append(subject_absentee_entry.report_datetime.strftime('%Y-%m-%d'))
        if not report_datetime:
            report_datetime.append('add new entry')
        return report_datetime
    absentee_form_label.allow_tags = True

#     @property
#     def undecided_form_url(self):
#         """Returns a url to the subject_undecided if an instance exists."""
#         url = ''
#         subject_undecided = None
#         if not self.registered_subject:
#             self.save()
#         SubjectUndecided = models.get_model('bcpp_subject', 'subjectundecided')
#         if SubjectUndecided.objects.filter(household_member=self):
#             subject_undecided = SubjectUndecided.objects.get(household_member=self)
#         if subject_undecided:
#             url = subject_undecided.get_absolute_url()
#         else:
#             url = SubjectUndecided().get_absolute_url()
#         return url
# 
#     @property
#     def undecided_form_label(self):
#         SubjectUndecided = models.get_model('bcpp_subject', 'subjectundecided')
#         SubjectUndecidedEntry = models.get_model('bcpp_subject', 'subjectundecidedentry')
#         report_datetime = []
#         if SubjectUndecided.objects.filter(household_member=self):
#             subject_undecided = SubjectUndecided.objects.get(household_member=self)
#             for subject_undecided_entry in SubjectUndecidedEntry.objects.filter(subject_undecided=subject_undecided).order_by('report_datetime'):
#                 report_datetime.append(subject_undecided_entry.report_datetime.strftime('%Y-%m-%d'))
#         if not report_datetime:
#             report_datetime.append('add new entry')
#         return report_datetime

    @property
    def refused_form_url(self):
        return self._get_form_url('subjectrefusal')

    @property
    def moved_form_url(self):
        return self._get_form_url('subjectmoved')

    def get_form_label(self, model_name):
        model = models.get_model('bcpp_subject', model_name)
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

    def cso(self):
        return self.household_structure.household.cso_number

    def lon(self):
        return self.household_structure.household.gps_lon

    def lat(self):
        return self.household_structure.household.gps_lat

    def to_locator(self):
        retval = ''
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('admin:bcpp_subject_subjectlocator_changelist')
                retval = '<a href="{0}?q={1}">locator</A>'.format(url, self.registered_subject.subject_identifier)
        return retval
    to_locator.allow_tags = True

#     def contact(self):
#         url = reverse('admin:bcpp_household_contactlog_add')
#         ret = """<a href="{url}" class="add-another" id="add_id_contact_log" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View contact"/>contact</a>""".format(url=url)
#         if self.contact_log:
#             url = self.contact_log.get_absolute_url()
#             ret = """<a href="{url}" class="add-another" id="change_id_contact_log" onclick="return showAddAnotherPopup(this);">contact</a>""".format(url=url)
#         return ret
#     contact.allow_tags = True

    def get_short_label(self):
        return '{first_name} ({initials}) {gender} {age} {hiv_status}'.format(
            first_name=mask_encrypted(self.first_name),
            initials=self.initials,
            age=self.age_in_years,
            gender=self.gender,
            hiv_status=self.get_hiv_history())

    def get_subject_identifier(self):
        """ Uses the hsm internal_identifier to locate the subject identifier in
        registered_subject OR return the hsm.pk"""
        if RegisteredSubject.objects.filter(registration_identifier=self.internal_identifier):
            registered_subject = RegisteredSubject.objects.get(registration_identifier=self.internal_identifier)
            subject_identifier = registered_subject.subject_identifier
            if not subject_identifier:
                subject_identifier = registered_subject.registration_identifier
        else:
            #$ this should not be an option as all hsm's have a registered_subject instance
            subject_identifier = self.pk
        return subject_identifier

    def consent(self):

        """ Gets the consent model instance else return None.

        The consent model is not known until an instance exists
        since this model is related to all consent models but the instance
        is only related to consent model instance.

        For the consent model, i decided not to use the "proxy" design
        as implemented for other "registration" models. This method
        helps get around that decision.
        """

        # determine related consent models
        related_object_names = [related_object.name for related_object in self._meta.get_all_related_objects() if 'consent' in related_object.name and 'audit' not in related_object.name]
        consent_models = [models.get_model(related_object_name.split(':')[0], related_object_name.split(':')[1]) for related_object_name in related_object_names]
        # search models
        consent_instance = None
        for consent_model in consent_models:
            if consent_model.objects.filter(household_member=self):
                consent_instance = consent_model.objects.get(household_member=self.pk)
                break
        return consent_instance

    def is_minor(self):
        return (self.age_in_years >= 16 and self.age_in_years <= 17)

    def is_adult(self):
        return (self.age_in_years >= 18 and self.age_in_years <= 64)

    def enrolment_checklist(self):
        EnrolmentChecklist = models.get_model('bcpp_household_member', 'EnrolmentChecklist')
        self.enrolment_checklist = []
        if EnrolmentChecklist.objects.filter(household_member=self):
            self.enrolment_checklist = EnrolmentChecklist.objects.get(household_member=self)
        return self.enrolment_checklist

    def is_eligible(self):
        "Returns if the subject is eligible or ineligible based on age"
        if self.is_minor():
            return True
        elif self.is_adult():
            return True
        else:
            return False

    def is_eligible_label(self):
        "Returns if the subject is eligible or ineligible based on age"
        if self.is_minor():
            return "Eligible Minor"
        elif self.is_adult():
            return "Eligible Adult"
        else:
            return "not eligible"

    def resident(self):
        if self.nights_out <= 3:
            return "permanent (%s)" % self.nights_out
        if self.nights_out > 3 and self.nights_out <= 14:
            return "partial (%s)" % self.nights_out
        if self.nights_out > 14:
            return "occasional (%s)" % self.nights_out
        else:
            return "no (%s)" % self.nights_out

    def member_terse(self):
        return mask_encrypted(unicode(self.first_name))

    def subject(self):
        return mask_encrypted(unicode(self.first_name))

    def visit_date(self):
        SubjectVisit = models.get_model('bcpp_subject', 'subjectvisit')
        retval = None
        if SubjectVisit.objects.filter(household_member=self):
            subject_visit = SubjectVisit.objects.filter(household_member=self)
            retval = subject_visit.report_datetime
        return retval

    def calendar_datetime(self):
        return self.created

    def calendar_label(self):
        return self.__unicode__()

    def deserialize_on_duplicate(self):
        """Lets the deserializer know what to do if a duplicate is found, handled, and about to be saved."""
        retval = False
        if (self.present.lower() == 'yes' or self.present.lower() == 'no'):
            if self.is_eligible_member and self.member_status:
                retval = True
            elif not self.is_eligible_member:
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
                    if HouseholdMember.objects.filter(pk=registered_subject.registration_identifier).exists():
                        retval = HouseholdMember.objects.get(pk=registered_subject.registration_identifier).household_structure
        return retval

    class Meta:
        ordering = ['-created']
        unique_together = (("household_structure", "first_name", "initials"), ('registered_subject', 'household_structure'))
        app_label = 'bcpp_household_member'
