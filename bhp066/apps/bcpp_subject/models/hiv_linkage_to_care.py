from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import COMMUNITY_NA

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


KEPT_APPT = (
    ('Yes', 'Yes, kept appointment'),
    ('No_refered_other_clinic', 'No but attended a visit at the HIV care clinic to which they were referred on another date'),
    ('No_other_clinic', 'No but attended a visit at a different HIV clinic'),
    ('diff_clininc', 'I went to a different clinic'),
    ('No', 'No but tried to attend an HIV care clinic and left before I saw a healthcare provider'),
    ('No', 'I have not been to any HIV care clinic [skip to #3]')
)

TYPE_OF_EVIDENCE = (
    ("self_report_only", "Self-Report Only"),
    ("opr_card", "OPD Card"),
    ("clinic_paperwork", "Clinic paperwork"),
    ("other", "Other ")
)

RECOMMENDED_THERAPY = (
    ("Yes", "Yes"),
    ("No", "No")
)

STARTERED_THERAPY = (
    ("Yes", "Yes"),
    ("No", "No")
)

REASON_RECOMMENDED = (
    ("low_cd4", "Low CD4"),
    ("high_viral_load", "High viral load"),
    ("pregnancy_breastfeeding", "Pregnancy or breastfeeding"),
    ("tuberculosis", "Tuberculosis"),
    ("cancer", "Cancer"),
    ("dnt_knw", "Do not know"),
)


class HivLinkageToCare (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    kept_appt = models.CharField(
        verbose_name="We last spoke with you on last_visit_date and scheduled an appointment for you "
                     "in an HIV care clinic on last_appt_date. Did you keep that appointment?",
        max_length=50,
        choices=KEPT_APPT,
        null=True,
        help_text="")

    diff_clininc = models.CharField(
        verbose_name='If went to a different clinic, specify clinic:',
        default=None,
        null=True,
        blank=True,
        max_length=50,
        help_text=""
    )

    left_clininc_datetime = models.DateField(
        verbose_name='If you tried to attend an HIV care clinic and left before You saw a healthcare provider specify the date?',
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    clinic_first_datetime = models.DateField(
        verbose_name="What was the date when you first went to the community_name clinic?",
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    evidence_type_clinic = models.CharField(
        verbose_name="Type of Evidence:",
        max_length=50,
        choices=TYPE_OF_EVIDENCE,
        null=True,
        help_text="")

    evidence_type_clinic_other = OtherCharField()

    recommended_therapy = models.CharField(
        verbose_name="[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] Since the last time we spoke with "
                     "you on last_visit_date, has a doctor/nurse or other healthcare worker recommended "
                     "that you start antiretroviral therapy (ARVs), a combination of medicines to treat your "
                     "HIV infection?",
        max_length=50,
        choices=RECOMMENDED_THERAPY,
        null=True,
        help_text="If No [SKIP TO #10]")

    reason_recommended = models.CharField(
        verbose_name="If yes, do you know why ARVs were recommended?",
        max_length=50,
        choices=REASON_RECOMMENDED,
        null=True,
        blank=True,
        help_text="")

    reason_recommended_other = OtherCharField()

    startered_therapy = models.CharField(
        verbose_name="[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] Did you [start/restart] ART since we "
                     "spoke with you on last_visit_date?",
        max_length=50,
        choices=STARTERED_THERAPY,
        null=True,
        help_text="If NO [SKIP TO #9]")

    startered_therapy_date = models.DateField(
        verbose_name="When did you [start/restart] ART?",
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    start_therapy_clininc = models.CharField(
        verbose_name="Which clinic facility did you [start/restart] ART at?",
        max_length=25,
        choices=COMMUNITY_NA,
        help_text="")

    start_therapy_clininc_other = OtherCharField()

    not_refered_clininc = models.CharField(
        verbose_name="[If Clinic is not the referred clinic] In which community is this clinic located",
        default=None,
        null=True,
        blank=True,
        max_length=50,
        help_text=""
    )

    evidence_not_refered = models.CharField(
        verbose_name="Type of Evidence:",
        max_length=50,
        choices=TYPE_OF_EVIDENCE,
        null=True,
        help_text="")

    evidence_not_refered_other = OtherCharField()

    history = AuditTrail()

    def previous_visit(self):
        """ Returns the next earlier subject_visit of the participant.
        e.g if visit time point is 3, then return time point 2 if it exists else time point 1.
        If no previous visit, then the current visit is returned."""
        from edc.subject.appointment.models import Appointment
        from ..models import SubjectVisit
        registered_subject = self.subject_visit.appointment.registered_subject
        timepoints = range(0, self.subject_visit.appointment.visit_definition.time_point)
        if len(timepoints) > 0:
            timepoints.reverse()
        for point in timepoints:
            try:
                previous_appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                               visit_definition__time_point=point)
                return SubjectVisit.objects.get(appointment=previous_appointment)
            except Appointment.DoesNotExist:
                pass
            except SubjectVisit.DoesNotExist:
                pass
            except AttributeError:
                pass
        return None

    def previous_appt(self):
        from edc.subject.appointment.models import Appointment
        registered_subject = self.subject_visit.appointment.registered_subject
        timepoints = range(0, self.subject_visit.appointment.visit_definition.time_point)
        if len(timepoints) > 0:
            timepoints.reverse()
        for point in timepoints:
            try:
                return Appointment.objects.get(registered_subject=registered_subject,
                                               visit_definition__time_point=point)
            except Appointment.DoesNotExist:
                pass
        return None

    def last_community(self):
        return self.subject_visit.household_member.household_structure.household.plot

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Hiv Linkage To Care"
        verbose_name_plural = "Hiv Linkage To Care"
