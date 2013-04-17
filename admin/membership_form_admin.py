from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from bhp_visit.models import MembershipForm


class MembershipFormAdmin (BaseModelAdmin):

    list_display = ('content_type_map', 'category', 'visible', 'user_created', 'user_modified', 'created', 'modified')

    list_filter = ('category',)

    search_fields = ('id',)

admin.site.register(MembershipForm, MembershipFormAdmin)
