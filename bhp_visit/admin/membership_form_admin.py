from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_visit.models import MembershipForm
from bhp_visit.forms import MembershipFormForm


class MembershipFormAdmin (BaseModelAdmin):

    form = MembershipFormForm

    list_display = ('content_type_map', 'category', 'visible', 'user_created', 'user_modified', 'created', 'modified')

    list_filter = ('category',)

    search_fields = ('id',)

admin.site.register(MembershipForm, MembershipFormAdmin)
