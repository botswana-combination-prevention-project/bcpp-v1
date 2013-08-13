from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from base_transaction import BaseTransaction


class OutgoingTransaction(BaseTransaction):

    """ transactions produced locally to be consumed/sent to a queue or consumer """
    is_consumed_middleman = models.BooleanField(
        default=False,
        db_index=True,
        )

    is_consumed_server = models.BooleanField(
        default=False,
        db_index=True,
        )

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.is_consumed_server and not self.consumed_datetime:
                self.consumed_datetime = datetime.today()
        super(OutgoingTransaction, self).save(*args, **kwargs)

    def render(self):
        url = reverse('view_transaction_url', kwargs={'model_name': self._meta.object_name.lower(), 'pk': self.pk})
        ret = """<a href="{url}" class="add-another" id="add_id_report" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View transaction"/></a>""".format(url=url)
        return ret
    render.allow_tags = True

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']
