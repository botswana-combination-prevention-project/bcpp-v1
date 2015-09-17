from django.db import models
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..models import Household


class HicEnrolledFilter(SimpleListFilter):

    title = _('Hic Enrolled')
    parameter_name = 'hic_enrolled'

    def lookups(self, request, model_admin):
        return (('Yes', 'Yes'), ('No', 'No'), )

    def queryset(self, request, queryset):
        HicEnrollment = models.get_model('bcpp_subject', 'HicEnrollment')
        # Household = models.get_model('bcpp_household', 'Household')
        # Plot = models.get_model('bcpp_household', 'Plot')
        not_enrolled = []
        enrolled = []
        if isinstance(queryset.all()[0], Household):
            for hs in queryset.all():
                if not HicEnrollment.objects.filter(hic_permission='Yes', subject_visit__household_member__household_structure__household=hs).exists():
                    enrolled.append(hs)
                else:
                    not_enrolled.append(hs)
            if self.value() == 'Yes':
                return queryset.filter(household_identifier__in=enrolled)
            if self.value() == 'No':
                return queryset.filter(household_identifier__in=not_enrolled)
        else:
            for hs in queryset.all():
                if not HicEnrollment.objects.filter(hic_permission='Yes', subject_visit__household_member__household_structure__household__plot=hs).exists():
                    enrolled.append(hs)
                else:
                    not_enrolled.append(hs)
            if self.value() == 'Yes':
                return queryset.filter(plot_identifier__in=enrolled)
            if self.value() == 'No':
                return queryset.filter(plot_identifier__in=not_enrolled)
