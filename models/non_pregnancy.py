from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import YES_NO_UNSURE
from base_pregnancy import BasePregnancy


class NonPregnancy (BasePregnancy):

    """CS002"""

    more_children = models.CharField(
        verbose_name=_("Do you wish to have a child now or in the future?"),
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_nonpregnancy_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Non Pregnancy"
        verbose_name_plural = "Non Pregnancy"
