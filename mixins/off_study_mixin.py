from datetime import datetime
from django.core.exceptions import ImproperlyConfigured


class OffStudyMixin(object):

    def get_off_study_cls(self):
        """Returns the model class of the local apps off study form."""
        raise ImproperlyConfigured('Method must be overridden to return the model class of the off study ModelForm. Model {0}'.format(self._meta.object_name))

    def _get_off_study_cls(self):
        from bhp_off_study.models import BaseOffStudy
        if isinstance(self, BaseOffStudy):
            return None
        return self.get_off_study_cls()

    def is_off_study(self):
        """Confirms an off-study form does not exist for this subject.

        Once consented, a subject must be deliberately taken "off study" using a model that
        is a subclass of bhp_off_study.models.base_off_study."""
        if not 'get_subject_identifier' in dir(self):
            raise ImproperlyConfigured('OffStudyMixin expected method \'get_subject_identifier\' to exist on the base model class. Model {0}'.format(self._meta.object_name))
        if not 'get_report_datetime' in dir(self):
            raise ImproperlyConfigured('OffStudyMixin expected method \'get_report_datetime\' to exist on the base model class. Model {0}'.format(self._meta.object_name))
        report_datetime = self.get_report_datetime()
        report_date = datetime(report_datetime.year, report_datetime.month, report_datetime.day)
        if self._get_off_study_cls():
            return self._get_off_study_cls().objects.filter(registered_subject__subject_identifier=self.get_subject_identifier(), offstudy_date__lt=report_date).exists()
        return False
