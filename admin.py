from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from models import Link
from forms import LinkForm


class LinkAdmin(BaseModelAdmin):
    form = LinkForm
    fields = (
        "label",
        "app_label",
        "dashboard_type",
        "ajax_method",
        "is_active")
    list_display = (
        "label",
        "app_label",
        "dashboard_type",
        "ajax_method",
        "is_active")

admin.site.register(Link, LinkAdmin)
