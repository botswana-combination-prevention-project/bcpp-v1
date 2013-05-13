from datetime import datetime, date
from django.db import models
from django.db.models import Max, get_app, get_models
from django.core.exceptions import ImproperlyConfigured
from bhp_base_model.fields import OtherCharField
from bhp_registration.models import BaseRegisteredSubjectModel
from bhp_crypto.utils import mask_encrypted
from bhp_off_study.managers import OffStudyManager
from bhp_off_study.exceptions import SubjectOffStudyDateError
from bhp_visit_tracking.models import BaseVisitTracking


class BaseOffStudy(BaseRegisteredSubjectModel):
    """Base model for the Off Study model in an app."""
    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        help_text="",
        )

    reason = models.CharField(
        verbose_name="Please code the primary reason participant taken off-study",
        max_length=30,
        # choices = OFF_STUDY_REASON,
        )

    reason_other = OtherCharField()

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments:",
        blank=True,
        null=True,
        )

    objects = OffStudyManager()

    def natural_key(self):
        return (self.offstudy_date, ) + self.registered_subject.natural_key()

    def get_report_datetime(self):
        return datetime(self.offstudy_date.year, self.offstudy_date.month, self.offstudy_date.day)

    def check_off_study_date(self, subject_identifier, off_study_date, exception_cls=None):
        """Checks that off study date is on or after the visit model visit_datetime."""
        if not subject_identifier:
            raise AttributeError('Attribute subject_identifier is required.')
        if not off_study_date:
            raise AttributeError('Attribute off_study_date is required.')
        if not exception_cls:
            exception_cls = SubjectOffStudyDateError
        app = get_app(self._meta.app_label)
        for model in get_models(app):
            if issubclass(model, BaseVisitTracking):
                # get max visit_datetime from visit model. model is the visit model
                agg = model.objects.filter(appointment__registered_subject__subject_identifier=subject_identifier).aggregate(Max('report_datetime'))
                max_report_datetime = agg.get('report_datetime__max', None)
                if max_report_datetime:
                    report_date = date(max_report_datetime.year, max_report_datetime.month, max_report_datetime.day)
                    if off_study_date < report_date:
                        raise exception_cls('Data exists for this subject with a report datetime AFTER the off study date of {0}. See {1} with report_datetime {2}.'.format(off_study_date, model._meta.object_name, max_report_datetime))

    def save(self, *args, **kwargs):
        self.check_off_study_date(self.get_subject_identifier(), self.offstudy_date)
        super(BaseOffStudy, self).save(*args, **kwargs)

    def post_save_clear_future_appointments(self):
        """Deletes appointments created after the off-study datetime if the appointment has no visit report."""
        Appointment = models.get_model('bhp_appointment', 'appointment')
        visit_model_cls = self.get_visit_model_cls()
        if not visit_model_cls:
            raise ImproperlyConfigured('Model {0} cannot determine the visit model class for the app'.format(self._meta.object_name))
        if visit_model_cls:
            for appointment in Appointment.objects.filter(
                    registered_subject=self.registered_subject,
                    appt_datetime__gt=self.offstudy_date):
                # only delete appointments that have no visit report
                if not visit_model_cls.objects.filter(appointment=appointment).exists():
                    appointment.delete()

    def __unicode__(self):
        return "{0} {1} ({2})".format(self.registered_subject.subject_identifier,
                                      self.registered_subject.subject_type,
                                      mask_encrypted(self.registered_subject.first_name))

    class Meta:
        app_label = 'bhp_off_study'
        abstract = True
