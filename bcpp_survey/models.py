from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify

from edc_base.model.models import BaseUuidModel

from .managers import SurveyManager


class Survey (BaseUuidModel):

    survey_name = models.CharField(
        verbose_name="Survey name",
        max_length=15,
        validators=[RegexValidator('BCPP\ Year\ [0-9]{1}'), ],
        help_text="format is, form example, BCPP Year 1",
        db_index=True,
        unique=True,
    )

    survey_abbrev = models.CharField(
        verbose_name="Survey name abbreviation",
        max_length=3,
        unique=True,
        null=True,
        blank=True,
    )

    survey_description = models.CharField(
        verbose_name="Description",
        max_length=15,
        help_text="",
        null=True,
        blank=True,
        db_index=True,
    )

    survey_slug = models.SlugField(max_length=40, db_index=True)

    chronological_order = models.IntegerField(default=0, db_index=True)

    datetime_start = models.DateTimeField(
        verbose_name="Start Date",
        help_text="",
    )

    datetime_end = models.DateTimeField(
        verbose_name="End Date",
        help_text="",
    )

    objects = SurveyManager()

    def natural_key(self):
        return (self.survey_name, )

    def __unicode__(self):
        return self.survey_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey_slug = slugify(self.survey_name)
        super(Survey, self).save(*args, **kwargs)

    @property
    def not_started(self):
        return self.datetime_start > datetime.today()

    def is_dispatchable_model(self):
        return True

    class Meta:
        app_label = 'bcpp_survey'
        ordering = ['survey_name', ]
