from django.contrib import admin
from datetime import date, timedelta, datetime
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from models import *
from forms import *


# Link
class LinkAdmin(MyModelAdmin): 

    form = LinkForm

    fields = (
        "label",
        "app_label",
        "dashboard_type",
        "ajax_method",
        "is_active"
    )

    list_display = (        
        "label",
        "app_label",
        "dashboard_type",        
        "ajax_method",
        "is_active",
    )

    radio_fields = {
        
    }

    filter_horizontal = (
        
    )

    """"""

admin.site.register(Link, LinkAdmin)
