from models import Result, ResultItem


def recalculate_grading(modeladmin, request, queryset):

    for qs in queryset:
        n = 0
        if isinstance(qs, Result):
            for result_item in ResultItem.objects.filter(result=qs):
                result_item.save()
                n += 1
            modeladmin.message_user(request, 'Recalculated grading and references for {0} items in result {1}'.format(n, qs.result_identifier))
        elif isinstance(qs, ResultItem):
            qs.save()
            modeladmin.message_user(request, 'Recalculated grading and references for item {0} of result {1}'.format(qs.test_code.code, qs.result))
        else:
            modeladmin.message_user(request, 'Nothing to do. Must be either a result or result item.')
            break
recalculate_grading.short_description = "Recalculate grading and references"


def flag_as_reviewed(modeladmin, request, queryset):
    for qs in queryset:
        qs.reviewed = True
        if not qs.review:
            qs.save()
        qs.review.review_status = 'REVIEWED'
        qs.review.save()
        qs.save()
flag_as_reviewed.short_description = "Review: flag as reviewed"


def unflag_as_reviewed(modeladmin, request, queryset):
    for qs in queryset:
        qs.reviewed = False
        if not qs.review:
            qs.save()
        qs.review.review_status = 'REQUIRES_REVIEWED'
        qs.review.save()
        qs.save()
unflag_as_reviewed.short_description = "Review: flag as NOT reviewed"
