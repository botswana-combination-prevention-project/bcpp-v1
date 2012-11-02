from lab_reference.models import BaseReferenceListItem


def flag_as_active(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, BaseReferenceListItem):
                modeladmin.message_user(request, 'Records must be a list item. (BaseReferenceListItem)')
                break
            else:
                if not qs.active:
                    qs.active = True
                    qs.save()
flag_as_active.short_description = "Flag reference item as active"


def flag_as_inactive(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, BaseReferenceListItem):
                modeladmin.message_user(request, 'Records must be a list item. (BaseReferenceListItem)')
                break
            else:
                if qs.active:
                    qs.active = False
                    qs.save()
flag_as_inactive.short_description = "Flag reference item as in-active"


def toggle_lln(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, BaseReferenceListItem):
                modeladmin.message_user(request, 'Records must be a list item. (BaseReferenceListItem)')
                break
            else:
                qs.use_lln = not qs.use_lln
                qs.save()
toggle_lln.short_description = "toggle LLN"


def toggle_uln(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, BaseReferenceListItem):
                modeladmin.message_user(request, 'Records must be a list item. (BaseReferenceListItem)')
                break
            else:
                qs.use_uln = not qs.use_uln
                qs.save()
toggle_uln.short_description = "toggle ULN"
