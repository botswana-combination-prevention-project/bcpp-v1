from django.utils.translation import ugettext as _
from bhp_base_model.models import BaseUuidModel
from bhp_base_model.fields import NameField, InitialsField


class SiteLeader (BaseUuidModel):

    first_name = NameField(
        verbose_name=_("First name")
        )

    last_name = NameField(
        verbose_name=_("Last name")
    )

    initials = InitialsField()

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return "/bhp_lab_registration/siteleader/%s/" % self.id

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['last_name', 'first_name']
        app_label = 'bhp_research_protocol'
