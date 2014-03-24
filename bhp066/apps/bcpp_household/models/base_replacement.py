from django.core.exceptions import ObjectDoesNotExist

from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..classes import ReplacementData
from ..exceptions import AlreadyReplaced


class BaseReplacement(BaseDispatchSyncUuidModel):

    def is_plot(self):
        return False

    def is_household(self):
        return False

    def replaced(self, using=None):
        return None

    def potential_replacement(self, using=None):
        plot = None
        if self.is_plot():
            plot = self
        elif self.is_household():
            plot = self.plot
        else:
            if self.replacement_container(using):
                plot = self.replacement_container(using).plot
        if ReplacementData().check_refusals(plot):
            for item in ReplacementData().check_refusals(plot):  #item is a household or a plot
                item[0].replaceble = True
                item[0].save()
        if ReplacementData().check_absentees_ineligibles(plot):
            for item in ReplacementData().check_absentees_ineligibles(plot):
                item[0].replaceble = True
                item[0].save()
        if ReplacementData().is_replacement_valid(plot):
            for item in ReplacementData().is_replacement_valid(plot):
                item[0].replaceble = True
                item[0].save()

    def replacement_container(self, using=None):
        if self.is_household():
            return self
        return None

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if not (self.is_plot() or self.is_household()):
            self.potential_replacement(using)
        if self.replacement_container(using):  # returns a household instance
            if self.id:
                try:
                    household = self.replacement_container(using).__class__.objects.get(household_identifier=self.replacement_container(using).household_identifier)
                    if household.replacement and household.replaceble:
                        raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
                except ObjectDoesNotExist:
                    pass
        if self.replaced(using):  # returns a plot instance
            if self.id:
                try:
                    plot = self.replaced(using).__class__.objects.get(plot_identifier=self.replaced(using).plot_identifier)
                    if plot.replacement and plot.replaceble:
                        raise AlreadyReplaced('Model {0}-{1} is replaced.'.format(self._meta.object_name, self.pk))
                except ObjectDoesNotExist:
                    pass
        super(BaseReplacement, self).save(*args, **kwargs)

    class Meta:
        abstract = True



