from datetime import date, timedelta, datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_is_future
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_lab.models import SubjectRequisition

from edc.map.classes import site_mappers

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .circumcision import Circumcision
from .hiv_care_adherence import HivCareAdherence
from .hiv_result import HivResult
from .hiv_test_review import HivTestReview
from .pima import Pima
from .residency_mobility import ResidencyMobility
from .reproductive_health import ReproductiveHealth
from .subject_consent import SubjectConsent
from .cd4_history import Cd4History

site_mappers.autodiscover()

REFERRAL_CODES = (
    ('TST-CD4', 'POS any, need CD4 testing'),
    ('HIV-IND', 'HIV re-test (IND)'),
    ('MASA', 'Known POS, MASA continued care'),
    ('MASA-DF', 'Known POS, MASA defaulter (was on ART)'),
    ('SMC-NEG', 'SMC'),
    ('NEG!-PR', 'NEG today, Pregnant'),
    ('POS!-PR', 'POS today, Pregnant'),
    ('POS#-AN', 'Known POS, Pregnant, on ART (ANC)'),
    ('POS#-PR', 'Known POS, Pregnant, not on ART'),
    ('POS!-HI', 'POS today, not on ART, high CD4)'),
    ('POS!-LO', 'POS today, not on ART, low CD4)'),
    ('POS#-HI', 'Known POS, not on ART, high CD4)'),
    ('POS#-LO', 'Known POS, not on ART, low CD4)'),
    ('NOT-REF', 'Not referred'),
    ('ERROR', 'Error'),
)


class BaseSubjectReferral(BaseScheduledVisitModel):

    class Meta:
        abstract = True


class SubjectReferral(BaseSubjectReferral, ExportTrackingFieldsMixin):

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        default=datetime.today(),
        help_text="... or next refill / clinic date if on ART."
        )

    referral_clinic = models.CharField(
        max_length=50,
        choices=COMMUNITIES,
        default=site_mappers.get_current_mapper().map_area,
        )

    referral_clinic_other = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        )

    gender = models.CharField(
        max_length=10,
        null=True,
        editable=False,
        )

    citizen = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        )

    hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        )

    hiv_result_datetime = models.DateTimeField(
         null=True,
         )

    new_pos = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="new POS diagnosis"
        )

    last_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        )

    last_hiv_test_date = models.DateTimeField(
         null=True,
         )

    last_cd4_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        )

    last_cd4_test_date = models.DateTimeField(
         null=True,
         )

    on_art = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="from hiv_care_adherence."
        )

    clinic_receiving_from = models.CharField(
        default=None,
        null=True,
        max_length=50,
        help_text="from hiv_care_adherence."
        )

    next_appointment_date = models.DateField(
         default=None,
         null=True,
         help_text="from hiv_care_adherence."
         )

    cd4_result = models.DecimalField(
        null=True,
        editable=False,
        max_digits=6,
        decimal_places=2,
        help_text='from Pima',
        )

    cd4_result_datetime = models.DateTimeField(
        null=True,
        help_text='from Pima',
        )

    vl_sample_drawn = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='from SubjectRequisition',
        )

    vl_sample_datetime_drawn = models.DateTimeField(
        null=True,
        help_text='from SubjectRequisition',
         )

    pregnant = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="from ReproductiveHealth.currently_pregnant",
        )

    circumcised = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        )

    permanent_resident = models.NullBooleanField(
        default=None,
        editable=False,
        null=True,
        help_text='from residence and mobility "permanent_resident"'
        )

    intend_residency = models.NullBooleanField(
        default=None,
        editable=False,
        null=True,
        help_text='from residence and mobility "intend_residency"'
        )

    referred_from_bhs = models.NullBooleanField(
        default=None,
        editable=False,
        null=True,
        help_text='referred by an RA',
        )

    urgent_referral = models.NullBooleanField(
        default=None,
        null=True,
        )

    referral_code = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        help_text="list of referral codes updated internally, comma separated."
        )

    in_clinic_flag = models.BooleanField(
        default=False,
        editable=False,
        help_text='flag indicating participant was seen in clinic (from implementer data.)'
        )

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment')
        )

    export_history = ExportHistoryManager()

    history = AuditTrail()

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.referral_code, self.referral_appt_date, self.referral_clinic)

    def save(self, *args, **kwargs):
        self.update_demographics()
        self.update_hiv()
        self.update_last_hiv()
        self.update_cd4()
        self.update_last_cd4()
        self.update_vl()
        self.update_residency()
        self.update_pregnant()
        self.update_circumcised()
        self.update_on_art()
        self.update_clinic_receiving_from()
        self.update_next_appointment_date()
        self.update_referral_code()
        self.update_urgent_referral()
        super(SubjectReferral, self).save(*args, **kwargs)

    def get_referral_identifier(self):
        return self.id

    def get_next_appt_date(self):
        if self.urgent_referral:
            return date.today()
        return date.today + timedelta(days=7)

    def update_demographics(self):
        self.gender = self.subject_visit.appointment.registered_subject.gender
        if SubjectConsent.objects.filter(household_member=self.subject_visit.household_member):
            subject_consent = SubjectConsent.objects.get(household_member=self.subject_visit.household_member)
            if subject_consent.identity_type == 'OMANG':
                self.citizen = True

    def update_hiv(self):
        if HivResult.objects.filter(subject_visit=self.subject_visit, hiv_result__in=['POS', 'NEG', 'IND']):
            hiv_result = HivResult.objects.get(subject_visit=self.subject_visit)
            self.hiv_result = hiv_result.hiv_result
            self.hiv_result_datetime = hiv_result.hiv_result_datetime
            if self.hiv_result == 'POS':
                self.new_pos = True
            elif self.hiv_result == 'NEG':
                self.new_pos = False
        else:
            self.hiv_result = None
            self.hiv_result_datetime = None
            self.new_pos = None

    def update_cd4(self):
        if Pima.objects.filter(subject_visit=self.subject_visit, pima_today='Yes'):
            pima = Pima.objects.get(subject_visit=self.subject_visit)
            self.cd4_result = int(pima.cd4_value)
            self.cd4_result_datetime = pima.cd4_datetime
        else:
            self.cd4_result = None
            self.cd4_result_datetime = None

    def update_last_hiv(self):
        if HivTestReview.objects.filter(subject_visit=self.subject_visit):
            hiv_test_review = HivTestReview.objects.get(subject_visit=self.subject_visit)
            self.last_hiv_result = hiv_test_review.recorded_hiv_result
            self.last_hiv_test_date = hiv_test_review.hiv_test_date
            self.new_pos = False
        else:
            self.last_hiv_result = None
            self.last_hiv_test_date = None
            self.new_pos = None

    def update_last_cd4(self):
        if Cd4History.objects.filter(subject_visit=self.subject_visit):
            cd4_history = Cd4History.objects.get(subject_visit=self.subject_visit)
            self.last_cd4_result = cd4_history.last_cd4_count
            self.last_cd4_test_date = cd4_history.last_cd4_drawn_date
        else:
            self.last_cd4_result = None
            self.last_cd4_test_date = None

    def update_vl(self):
        if SubjectRequisition.objects.filter(subject_visit=self.subject_visit, panel__edc_name='viral load'):
            if SubjectRequisition.objects.filter(subject_visit=self.subject_visit, panel__edc_name='viral load').count() > 1:
                #  FIXME: should not be possible, but dashboard still allows this (more than one req.per visit)
                subject_requisition = SubjectRequisition.objects.filter(subject_visit=self.subject_visit, panel__edc_name='viral load').order_by('created')[0]
            else:
                subject_requisition = SubjectRequisition.objects.get(subject_visit=self.subject_visit, panel__edc_name='viral load')
            if subject_requisition.is_drawn == 'Yes':
                self.vl_sample_drawn = True
                self.vl_sample_datetime_drawn = subject_requisition.drawn_datetime
            else:
                self.vl_sample_drawn = False
                self.vl_sample_datetime_drawn = None

    def update_residency(self):
        if ResidencyMobility.objects.filter(subject_visit=self.subject_visit):
            residency_mobility = ResidencyMobility.objects.get(subject_visit=self.subject_visit)
            self.permanent_resident = self.convert_to_nullboolean(residency_mobility.permanent_resident)
            self.intend_residency = self.convert_to_nullboolean(residency_mobility.intend_residency)
        else:
            self.permanent_resident = None
            self.intend_residency = None

    def update_circumcised(self):
        if self.gender == 'M':
            if Circumcision.objects.filter(subject_visit=self.subject_visit, circumcised='Yes'):
                self.circumcised = True
            elif Circumcision.objects.filter(subject_visit=self.subject_visit, circumcised='No'):
                self.circumcised = False
        else:
            self.circumcised = None

    def update_pregnant(self):
        if self.gender == 'F':
            if ReproductiveHealth.objects.filter(subject_visit=self.subject_visit):
                reproductive_health = ReproductiveHealth.objects.get(subject_visit=self.subject_visit)
                if reproductive_health.currently_pregnant == 'Yes':
                    self.pregnant = True
                if reproductive_health.currently_pregnant == 'No':
                    self.pregnant = False
        else:
            self.pregnant = None

    def update_on_art(self):
        if HivCareAdherence.objects.filter(subject_visit=self.subject_visit):
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            self.on_art = hiv_care_adherence.on_art()
        else:
            self.on_art = None

    def update_clinic_receiving_from(self):
        if HivCareAdherence.objects.filter(subject_visit=self.subject_visit):
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            self.clinic_receiving_from = hiv_care_adherence.clinic_receiving_from()
        else:
            self.clinic_receiving_from = None

    def update_next_appointment_date(self):
        if HivCareAdherence.objects.filter(subject_visit=self.subject_visit):
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            self.next_appointment_date = hiv_care_adherence.next_appointment_date()
        else:
            self.next_appointment_date = None

    def is_defaulter(self):
        if HivCareAdherence.objects.filter(subject_visit=self.subject_visit):
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            return hiv_care_adherence.defaulter()
        return False

    def update_urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        urgent_referral = False
        urgent_referral_codes = ['MASA-DF', 'POS!-LO', 'POS#-LO']
        if [code for code in self.get_referral_codes_as_list() if code in urgent_referral_codes]:
            urgent_referral = True
        self.urgent_referral = urgent_referral

    def get_referral_codes_as_list(self):
        return [x for x in self.referral_code.split(',')]

    def append_to_referral_code(self, value):
        referral_codes = []
        if value:
            referral_codes = [value]
            if self.referral_code:
                referral_codes.extend([item for item in self.get_referral_codes_as_list() if item != value])
                referral_codes.append(value)
        referral_codes.sort()
        self.referral_code = ';'.join(referral_codes)

    def update_referral_code(self):
        """Reviews the conditions for referral and sets to the correct referral code.

        MASA-LO: On ARVs but CD4 is low. Requires action.
        MASA-HI: On ARVs, CD4 is high.
        MAMO-LO: Not on ARV, low CD4"""
        self.referral_code = None
        if self.hiv_result:
            if self.hiv_result == 'IND':
                self.append_to_referral_code('HIV-IND')
            elif self.hiv_result == 'NEG' and self.pregnant:
                self.append_to_referral_code('NEG!-PR')
            elif self.hiv_result == 'NEG' and self.gender == 'F' and not self.pregnant:
                self.append_to_referral_code(None)
            elif self.hiv_result == 'POS' and self.pregnant and self.on_art == True:
                self.append_to_referral_code('ERROR')
            elif self.hiv_result == 'POS' and self.pregnant and self.on_art == False:
                self.append_to_referral_code('POS!-PR')
            elif self.hiv_result == 'POS' and self.pregnant and self.on_art == None:
                self.append_to_referral_code('POS!-PR')
            elif self.hiv_result == 'NEG' and self.circumcised == False:
                self.append_to_referral_code('SMC-NEG')
            elif self.hiv_result == 'POS':
                if self.on_art == True or self.on_art == False:
                    self.append_to_referral_code('ERROR')
                elif self.on_art == None:
                    if not self.cd4_result:
                        self.append_to_referral_code('TST-CD4')
                    elif self.cd4_result > 350:
                        self.append_to_referral_code('POS!-HI')
                    elif self.cd4_result <= 350:
                        self.append_to_referral_code('POS!-LO')
        elif self.last_hiv_result == 'POS':
            if self.is_defaulter():
                self.append_to_referral_code('MASA-DF')
            elif self.on_art:
                if self.pregnant:
                    self.append_to_referral_code('POS#-AN')
                elif not self.cd4_result:
                    self.append_to_referral_code('MASA')
                elif self.cd4_result > 350:
                    self.append_to_referral_code('ERROR')
                elif self.cd4_result <= 350:
                    self.append_to_referral_code('ERROR')
            elif not self.on_art:
                if self.pregnant:
                    self.append_to_referral_code('POS#-PR')
                elif not self.cd4_result:
                    self.append_to_referral_code('TST-CD4')
                elif self.cd4_result > 350:
                    self.append_to_referral_code('POS#-HI')
                elif self.cd4_result <= 350:
                    self.append_to_referral_code('POS#-LO')

        if not self.referral_code:
            self.append_to_referral_code('NOT-REF')
        if self.referral_code not in [item[0] for item in REFERRAL_CODES]:
            raise TypeError('Expected referral code to be one of {0}. Got {1}'.format([item[0] for item in REFERRAL_CODES], self.referral_code))

    def survey(self):
        return self.subject_visit.household_member.household_structure.survey
    survey.allow_tags = True

    def convert_to_nullboolean(self, yes_no_dwta):
        if str(yes_no_dwta) in ['True', 'False', 'None']:
            return yes_no_dwta
        if yes_no_dwta.lower() == 'no':
            return False
        elif yes_no_dwta.lower() == 'yes':
            return True
        else:
            return None

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.subject_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.subject_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Referral'
