from django.template.loader import render_to_string

from lab_clinic_api.models import Result, Order
from lab_clinic_api.classes import Lis


class EdcLab(object):

    def update(self, subject_identifier):
        lis = Lis('lab_api')
        last_updated = lis.update_from_lis(subject_identifier=subject_identifier)
        return last_updated

    def render(self, subject_identifier, update=False):
        # prepare results for dashboard sidebar
        last_updated = None
        if update:
            last_updated = self.update(subject_identifier)
        resulted = Result.objects.filter(order__aliquot__receive__registered_subject__subject_identifier=subject_identifier).order_by('-order__aliquot__receive__drawn_datetime')
        ordered = (Order.objects.filter(aliquot__receive__registered_subject__subject_identifier=subject_identifier)
                                .exclude(order_identifier__in=[result.order.order_identifier for result in resulted])
                                .order_by('-aliquot__receive__drawn_datetime'))
        return render_to_string('result_status_bar.html', {'resulted': resulted, 'ordered': ordered, 'last_updated': last_updated})
