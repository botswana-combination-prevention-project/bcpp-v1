#from django.contrib import messages
#from django.core.exceptions import ImproperlyConfigured
from models import ResultItem


def recalculate_grading(modeladmin, request, queryset):

    for result in queryset:
        n = 0
        for result_item in ResultItem.objects.filter(result=result):
            result_item.save()
            n += 1
        modeladmin.message_user(request, 'Recalculated grading and references for {0} items in result {1}'.format(n, result.result_identifier))

recalculate_grading.short_description = "Recalculate grading and references"
