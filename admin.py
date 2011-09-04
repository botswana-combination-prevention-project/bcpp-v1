from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Q
from datetime import date, timedelta, datetime
from bhp_common.models import MyModelAdmin, MyStackedInline, MyTabularInline
from forms import LabForm
from models import LocalResult

# Lab
class LocalResultAdmin(MyModelAdmin): 

    form = LocalResultForm

    fields = (
        "subject_identifier",
        "review_status",
        "review_datetime",
        "release_status",
        "panel",
        "aliquot_identifier",
        "receive_datetime",
        "receive_identifier",
        "drawn_datetime",
        "order_identifier",
        "release_datetime"
    )

    radio_fields = {
        "review_status":admin.VERTICAL
    }

    filter_horizontal = (
        
    )

    """"""

admin.site.register(LocalResult, LocalResultAdmin)
