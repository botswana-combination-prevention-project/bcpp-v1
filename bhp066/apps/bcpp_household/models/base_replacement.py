from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..classes import ReplacementData
from ..exceptions import AlreadyReplaced


class BaseReplacement(BaseDispatchSyncUuidModel):

    def is_plot(self):
        return False

    def is_household(self):
        return False

    def replaced(self, using=None):
        if self.is_household() or self.is_plot():
            if self.replacement:
                return True
        return False

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
        if self.is_plot() or self.is_household():
            return self
        return None

    def save(self, *args, **kwargs):
        using = kwargs.get('using', None)
        if not (self.is_plot() or self.is_household()):
            self.potential_replacement(using=None)
            # TODO: figure out a way here.
#         if self.replacement_container(using).replacement:
#             raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
#         if self.replaced(using):
#             raise AlreadyReplaced('Model {0}-{1} is replaced.'.format(self._meta.object_name, self.pk))
        super(BaseReplacement, self).save(*args, **kwargs)

    class Meta:
        abstract = True



