from datetime import date, timedelta

from django.conf import settings
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_is_future

from apps.bcpp.choices import COMMUNITIES

from .base_scheduled_visit_model import BaseScheduledVisitModel

REFERRAL_CODES = (
    ('CD4', 'POS, need CD4 testing'),
    ('HIV', 'HIV re-test (IND)'),
    ('MASA-HIGH', 'MASA continued care (on ART, high CD4)'),
    ('MASA-LOW', 'MASA continued care (on ART, low CD4)'),
    ('CCC-HIGH', 'CCC or MASA (not on ART, high CD4)'),
    ('CCC-LOW', 'CCC or MASA (not on ART, low CD4)'),
    ('SMC', 'SMC'),
)


class SubjectReferral(BaseScheduledVisitModel):

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        default=date.today(),
        help_text="...or next refill date if on ART."
        )

    referral_clinic = models.CharField(
        max_length=50,
        choices=COMMUNITIES,
        default=settings.CURRENT_COMMUNITY,
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
        )

    cd4_result = models.IntegerField(
        null=True,
        editable=False,
        )

    cd4_result_datetime = models.DateTimeField(
         null=True,
         )

    pregnant = models.NullBooleanField(
        default=False,
        null=True,
        editable=False,
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

    referral_code_list = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        help_text="list of referral codes updated internally"
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

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.update_urgent_referral()
        self.update_referral_codes()
        super(SubjectReferral, self).save(*args, **kwargs)

    def append_to_referral_codes(self, value):
        codes = []
        if value:
            codes = [value]
            if self.referral_code_list:
                codes = [x for x in self.referral_code_list.split(',')]
                codes.extend([item for item in codes if item != value])
                codes.append(value)
        self.referral_code_list = ','.join(codes)

    def get_next_appt_date(self):
        if self.urgent_referral():
            return date.today()
        return date.today + timedelta(days=7)

    def update_urgent_referral(self):
        urgent_referral = False
        if self.hiv_result == 'IND':
            urgent_referral = True
        elif self.hiv_result == 'POS':
            if self.on_art == None and self.cd4_result == None:
                urgent_referral = True
            elif self.cd4_result <= 350:
                urgent_referral = True
        self.urgent_referral = urgent_referral

    def update_referral_codes(self):
        if self.hiv_result == 'IND':
            self.append_to_referral_codes('HIV')
        elif self.hiv_result == 'NEG' and self.gender == 'F':
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

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Referral'
