from django.db import models
from bhp_adverse.models import DeathCauseInfo, DeathCauseCategory, DeathMedicalResponsibility, DeathReasonHospitalized
from bhp_base_model.fields import OtherCharField
from bhp_common.choices import YES_NO
from bhp_base_model.validators import date_not_before_study_start, date_not_future
from base_base_death import BaseBaseDeath


class BaseDeath(BaseBaseDeath):

    death_medical_responsibility = models.ForeignKey(
        DeathMedicalResponsibility,
        verbose_name="Who was responsible for primary medical care of the participant during the month prior to death?",
        help_text="")

    class Meta:
        abstract = True
