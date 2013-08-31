from django.db import models
from django.core.urlresolvers import reverse
from bhp_base_model.models import BaseUuidModel
from bhp_registration.models import RegisteredSubject


class BaseHistoryModel(BaseUuidModel):
    """...note:: no need to add this to sync, data is generated and will regenerate
                 on demand."""
    subject_identifier = models.CharField(max_length=25, db_index=True)
    report_datetime = models.DateTimeField(null=True, db_index=True)
    subject_type = models.CharField(max_length=25, null=True)
    group_name = models.CharField(max_length=25)
    test_code = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    value_datetime = models.DateTimeField()
    source_model_name = models.CharField(max_length=50)
    source_app_label = models.CharField(max_length=50, null=True, blank=False)
    source_identifier = models.CharField(max_length=50, null=True)
    history_datetime = models.DateTimeField(null=True)
    #registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    def __unicode__(self):
        return '{0}-{1}-{2}-{3}-{4}-{5}'.format(self.subject_type, self.subject_identifier, self.test_code, self.value, self.value_datetime, self.pk)

    def get_registered_subject(self):
        if RegisteredSubject.objects.filter(subject_identifier=self.subject_identifier):
            return RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
        return None

    def dashboard(self):
        ret = None
        if self.get_registered_subject():
            if self.get_registered_subject().subject_identifier:
                    url = reverse('subject_dashboard_url',
                                  kwargs={'dashboard_type': self.get_registered_subject().subject_type.lower(),
                                          'dashboard_model': 'registered_subject',
                                          'dashboard_id': self.get_registered_subject().pk,
                                          'show': 'appointments'})
                    ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        abstract = True
