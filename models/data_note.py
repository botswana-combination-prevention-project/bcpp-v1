from datetime import date, timedelta
from django.db import models
from django.core.urlresolvers import reverse
from bhp_crypto.fields import EncryptedTextField
from bhp_registration.models import RegisteredSubject
from bhp_base_model.models import BaseModel


class DataNote(BaseModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""
    registered_subject = models.ForeignKey(RegisteredSubject)
    subject = models.CharField(max_length=50, unique=True)
    comment_date = models.DateField(default=date.today())
    expiration_date = models.DateField(default=date.today() + timedelta(days=90), help_text='Data note will automatically be set to \'Resolved\' in 90 days unless otherwise specified.')
    comment = EncryptedTextField(max_length=500)
    display_on_dashboard = models.BooleanField(default=True)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('dashboard_url',
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                                       'subject_identifier': self.registered_subject.subject_identifier})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = "bhp_data_manager"
