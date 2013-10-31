from datetime import date, timedelta, datetime

from django.conf import settings
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_is_future
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin

from apps.bcpp.choices import COMMUNITIES

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .hiv_care_adherence import HivCareAdherence
from .reproductive_health import ReproductiveHealth

REFERRAL_CODES = (
    ('CD4', 'POS, need CD4 testing'),
    ('HIV', 'HIV re-test (IND)'),
    ('MASA-HIGH', 'MASA continued care (on ART, high CD4)'),
    ('MASA-LOW', 'MASA continued care (on ART, low CD4)'),
    ('MASA-DEFAULTER', 'MASA defaulter (was on ART)'),
    ('CCC-HIGH', 'CCC or MASA (not on ART, high CD4)'),
    ('CCC-LOW', 'CCC or MASA (not on ART, low CD4)'),
    ('SMC', 'SMC'),
    ('NOT_REFERED', 'Not referred'),
)

# TODO: defaulters


class SubjectReferral(BaseScheduledVisitModel, ExportTrackingFieldsMixin):

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        default=datetime.today(),
        help_text="... or next refill / clinic date if on ART."
        )

    referral_clinic = models.CharField(
        max_length=50,
        choices=COMMUNITIES,
        default=settings.CURRENT_COMMUNITY,
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
        default=False,
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

    on_art = models.NullBooleanField(
        default=False,
        null=True,
        editable=False,
        help_text="from hiv_care_adherence"
        )

    cd4_result = models.IntegerField(
        null=True,
        editable=False,
        )

    cd4_result_datetime = models.DateTimeField(
         null=True,
         )

    vl_sample_drawn = models.NullBooleanField(
        default=False,
        null=True,
        editable=False,
        )

    vl_sample_datetime_drawn = models.DateTimeField(
         null=True,
         )

    pregnant = models.NullBooleanField(
        default=False,
        null=True,
        editable=False,
        help_text="from ReproductiveHealth.currently_pregnant",
        )

    circumcised = models.NullBooleanField(
        default=False,
        null=True,
        editable=False,
        )

    permanent_resident = models.BooleanField(
        default=False,
        editable=False,
        help_text='from residence and mobility "permanent_resident"'
        )

    intend_residency = models.BooleanField(
        default=False,
        editable=False,
        help_text='from residence and mobility "intend_residency"'
        )

    urgent_referral = models.NullBooleanField(
        default=False,
        null=True,
        )

    referral_codes = models.CharField(
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
        return '{0} {1} {2}'.format(self.referral_codes, self.referral_appt_date, self.referral_clinic)

    def save(self, *args, **kwargs):
        self.update_pregnant()
        self.update_on_art()
        self.update_referral_codes()
        self.update_urgent_referral()
        super(SubjectReferral, self).save(*args, **kwargs)

    def get_referral_identifier(self):
        return self.id

    def get_next_appt_date(self):
        if self.urgent_referral():
            return date.today()
        return date.today + timedelta(days=7)

    def update_pregnant(self):
        if ReproductiveHealth.objects.filter(subject_visit=self.subject_visit):
            reproductive_health = ReproductiveHealth.objects.get(subject_visit=self.subject_visit)
            if reproductive_health.currently_pregnant == 'Yes':
                self.pregnant = True
            if reproductive_health.currently_pregnant == 'No':
                self.pregnant = False

    def update_on_art(self):
        if HivCareAdherence.objects.filter(subject_visit=self.subject_visit):
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            self.on_art = hiv_care_adherence.on_arv()

    def update_urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals list and sets to true on a match."""
        urgent_referral = False
        urgent_referral_codes = ['MASA-DEFAULTER', 'CCC-LOW', 'CCC-HIGH', 'HIV', 'CD4']
        if [code for code in self.get_referral_codes_as_list() if code in urgent_referral_codes]:
            urgent_referral = True
        self.urgent_referral = urgent_referral

    def get_referral_codes_as_list(self):
        return [x for x in self.referral_codes.split(',')]

    def append_to_referral_codes(self, value):
        codes = []
        if value:
            codes = [value]
            if self.referral_codes:
                codes = self.get_referral_codes_as_list()
                codes.extend([item for item in codes if item != value])
                codes.append(value)
        codes.sort()
        self.referral_codes = ','.join(codes)

    def update_referral_codes(self):
        """Reviews the conditions for referral and sets to the correct referral code."""
        if self.hiv_result == 'IND':
            self.append_to_referral_codes('HIV')
        elif self.hiv_result == 'NEG' and self.gender == 'F' and self.pregnant:
            self.append_to_referral_codes('ANC-NEG')
        elif self.hiv_result == 'POS' and self.gender == 'F' and self.pregnant:
            self.append_to_referral_codes('ANC-POS')
        elif self.hiv_result == 'NEG' and self.gender == 'F' and not self.pregnant:
            self.append_to_referral_codes(None)
        elif self.hiv_result == 'NEG' and self.gender == 'M':
            self.append_to_referral_codes('SMC')
        elif self.hiv_result == 'POS':
            if self.on_art:
                if self.cd4_result > 350:
                    self.append_to_referral_codes('MASA-HIGH')
                elif self.cd4_result <= 350:
                    self.append_to_referral_codes('MASA-LOW')
            elif not self.on_art:
                if not self.cd4_result:
                    self.append_to_referral_codes('CD4')
                if self.cd4_result > 350:
                    self.append_to_referral_codes('CCC-HIGH')
                elif self.cd4_result <= 350:
                    self.append_to_referral_codes('CCC-LOW')
        if not self.referral_codes:
            self.referral_codes = 'NOT_REFERRED'

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Referral'
