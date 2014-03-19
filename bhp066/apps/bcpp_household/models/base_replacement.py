from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..exceptions import AlreadyReplaced
from .household import Household
from .plot import Plot
from ..classes import ReplacementData


class BaseReplacement(BaseDispatchSyncUuidModel):

    history = AuditTrail()

    def replaced(self, using=None):
        if isinstance(Household, self.instance) or isinstance(Plot, self.instance):
            if self.instance.replacement:
                return True
        elif self.replacement_container(self, using=None).replacement:
            return True
        return False

    def potential_replacement(self, using=None):
        plot = None
        if isinstance(Plot, self.instance):
            plot = self.instance
        elif isinstance(Household, self.instance):
            plot = self.plot
        else:
            if self.replacement_container(using):
                plot = self.replacement_container(using).plot
        if ReplacementData().replace_refusals(plot):
            for item in ReplacementData().replace_refusals(plot):
                item.replaceble = True
                item.save()
        if ReplacementData().replacement_absentees_ineligibles(plot):
            for item in ReplacementData().replacement_absentees_ineligibles(plot):
                item.replaceble = True
                item.save()
        if ReplacementData().is_replacement_valid(plot):
            for item in ReplacementData().is_replacement_valid(plot):
                item.replaceble = True
                item.save()

    def replacement_container(self, using=None):
        return None

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'plot__plot_identifier')

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if self.id:
            if self.replacement_container(using):
                raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
            if self.replaced(using):
                raise AlreadyReplaced('Model {0}-{1} is replaced.'.format(self._meta.object_name, self.pk))
        super(BaseReplacement, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['-household_identifier', ]
