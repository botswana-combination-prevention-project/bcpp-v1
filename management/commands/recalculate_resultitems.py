import re
from django.core.management.base import BaseCommand
from lab_clinic_api.models import Result, ResultItem
from lab_result_item.classes import ResultItemFlag


class Command(BaseCommand):

    args = ()
    help = 'Recalculate grading and reference range flags for result items.'

    def handle(self, *args, **options):
        tot = Result.objects.all().count()
        result_count = 0
        for result in Result.objects.all().order_by('result_identifier'):
            n = 0
            for result_item in ResultItem.objects.filter(result=result):
                value = None
                if re.search(r'\d+\.?\d*', result_item.result_item_value):
                    try:
                        value = float(result_item.result_item_value)
                    except:
                        value = None
                if value:
                    result_item, modified = ResultItemFlag().calculate(result_item)
                    if modified:
                        result_item.save()
                    n += 1
            result_count += 1
            print ('{0} / {1} Recalculated for {2} items in result {3}'.format(result_count, tot, n, result.result_identifier))
