from datetime import date, timedelta, datetime

from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_is_future
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES


from ..choices import REFERRAL_CODES
from ..classes import SubjectReferralHelper
from ..managers import ScheduledModelManager

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .tb_symptoms import TbSymptoms

site_mappers.autodiscover()


class SubjectReferral(BaseScheduledVisitModel, ExportTrackingFieldsMixin):

    subject_referred = models.CharField(
        max_length=10,
        choices=(('Yes', 'Yes, subject has been handed a referral letter'),
                 ('No', 'No, subject has not been handed a referral letter'),
                 ('refused', 'Subject refused referral the referral letter')),
                )

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        default=datetime.today(),
        help_text="... or next refill / clinic date if on ART."
        )

    referral_clinic = models.CharField(
        max_length=50,
        choices=COMMUNITIES,
        #default=site_mappers.get_current_mapper().map_area,
        help_text='Subject has been referred to this clinic. If other specify below.'
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

    citizen_spouse = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        )

    hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='HIV status as determined by the field RA either by testing or using a combination of verbal response and documentation. See alos new_pos.'
        )

    hiv_result_datetime = models.DateTimeField(
         null=True,
        help_text='HIV result datetime either from today\'s test or documentation provided by the subject . See also new_pos.'
         )

    new_pos = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="True if subject is newly diagnosed POS"
        )

    last_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text="A documented previous HIV result provided by the subject"
        )

    verbal_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='from HivTestingHistory.verbal_result. HIV status as verbally provided by subject. See also if this result is supported by direct and indirect documentation.'
        )

    direct_hiv_documentation = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='from HivTestingHistory.has_record. A document that confirms the subject\'s verbally provided POS result. See also last_hiv_result.'
        )

    indirect_hiv_documentation = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='from HivTestingHistory.other_record. A document that suggests the subject is HIV POS.'
        )

    last_hiv_result_date = models.DateTimeField(
         null=True,
         )

#     last_cd4_result = models.CharField(
#         max_length=50,
#         null=True,
#         editable=False,
#         )
# 
#     last_cd4_test_date = models.DateTimeField(
#          null=True,
#          )

    on_art = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="from hiv_care_adherence. True if subject claims to be on ARV. See also art_documentation."
        )

    arv_documentation = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='from HivCarAdherence.arv_evidence. Yes if Field RA has seen documents that shows subject is on ARV\'s. Overrides on_art value if Yes')

    arv_clinic = models.CharField(
        default=None,
        null=True,
        max_length=50,
        help_text="from hiv_care_adherence. The ARV clinic where subject currently receives care"
        )

    next_arv_clinic_appointment_date = models.DateField(
         default=None,
         null=True,
         help_text="from hiv_care_adherence. Next appointment date at the subject's ARV clinic."
         )

    cd4_result = models.DecimalField(
        null=True,
        editable=False,
        max_digits=6,
        decimal_places=2,
        help_text='from Pima. Today\'s CD4 result',
        )

    cd4_result_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='from Pima',
        )

    vl_sample_drawn = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='from SubjectRequisition. True if a viral load sample was drawn in the household',
        )

    vl_sample_drawn_datetime = models.DateTimeField(
        null=True,
        editable=False,
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

    tb_symptoms = models.CharField(
        max_length=100,
        null=True,
        editable=False,
        help_text='list of symptoms from tb_symptoms'
        )

    urgent_referral = models.NullBooleanField(
        default=None,
        null=True,
        )

    referral_code = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        default='pending',
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

    objects = ScheduledModelManager()

    def __unicode__(self):
        return '{0}: {1} {2} {3}'.format(self.get_subject_identifier(), self.referral_code, self.referral_appt_date, self.referral_clinic)

    def save(self, *args, **kwargs):
        #if not self.referral_clinic:
        #    self.referral_clinic = site_mappers.get_current_mapper().map_area
        self.tb_symptoms = TbSymptoms.objects.get_symptoms(self.subject_visit)
        #self.referral_code = SubjectReferralHelper(self).referral_code
        for field, value in SubjectReferralHelper(self).subject_referral.iteritems():
            setattr(self, field, value)
        super(SubjectReferral, self).save(*args, **kwargs)

    def get_referral_identifier(self):
        return self.id

    def get_next_appt_date(self):
        if self.urgent_referral:
            return date.today()
        return date.today + timedelta(days=7)

    def survey(self):
        return self.subject_visit.household_member.household_structure.survey
    survey.allow_tags = True

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


class SubjectReferralReview(SubjectReferral):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = 'bcpp_subject'
        proxy = True