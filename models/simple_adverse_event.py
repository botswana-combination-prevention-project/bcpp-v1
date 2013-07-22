from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from bhp_base_model.models import BaseListModel
from bhp_consent.models import BaseConsentedUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_adverse.choices import GRADING_SCALE

""" list tables to be populated by study specific fixtures """


class AdverseEventReportType (BaseListModel):

    class Meta:
        app_label = "bhp_adverse"
        ordering = ['display_index']


class AdverseEventStudyRelation (BaseListModel):
    class Meta:
        app_label = "bhp_adverse"
        ordering = ['display_index']


class Ae010ReportType (BaseListModel):
    class Meta:
        app_label = "bhp_adverse"
        ordering = ['display_index']


class Ae010AdverseStudyRel (BaseListModel):
    class Meta:
        app_label = "bhp_adverse"
        ordering = ['display_index']


class SimpleAdverseEvent (BaseConsentedUuidModel):

    registered_subject = models.ForeignKey(RegisteredSubject)

    report_type = models.ForeignKey(Ae010ReportType,
        verbose_name=_("1. Which type of report is this?"),
        help_text="",
        )

    date_onset = models.DateField(
        verbose_name=_("2. Date of onset of event being reported here"),
        help_text="Format is YYYY-MM-DD",
        )

    ae_desc = models.TextField(
        max_length=250,
        verbose_name=_("3. Describe the \'adverse event\' and its relation to study activities"),
        help_text="",
        )

    event_grade = models.IntegerField(
        verbose_name="4. Grade of primary event ",
        help_text=_("Use grading scale 1-5, where 5 is death"),
        choices=GRADING_SCALE,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
            ]
        )

    adverse_study_rel = models.ForeignKey(Ae010AdverseStudyRel,
        verbose_name="5. Please describe the relationship between this adverse event and study activities",
        help_text="",
        )

    study_coord = models.CharField(
        max_length=35,
        verbose_name="6. Study coordinator",
        help_text="",
        )

    class Meta:
        app_label = "bhp_adverse"
