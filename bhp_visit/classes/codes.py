from django.db.models import Count
from bhp_visit.models import VisitDefinition


class VisitCodes(object):
    """
    visit_codes = VisitCodes()
    visit_codes.list(membership_form_category)
    """
    def list(self, membership_form_category):
        self._set_list(membership_form_category)
        return self._list

    def _set_list(self, membership_form_category):
        """Returns a list of visit codes for a membership form category."""
        if membership_form_category:
            raise AttributeError('Expected attribute \'membership_form_category\'. Got None')
        self._list = []
        agg = VisitDefinition.objects.values('code').filter(schedule_group__membership_form__category=membership_form_category).annotate(cnt=Count('code'))
        for dct in agg:
            self._list.append(dct['code'])
