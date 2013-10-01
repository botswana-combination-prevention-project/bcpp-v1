from django.contrib import admin
from ..models import HtcSubjectLocator
from ..forms import HtcSubjectLocatorForm
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin


class HtcSubjectLocatorAdmin(HtcSubjectVisitModelAdmin):

    form = HtcSubjectLocatorForm

admin.site.register(HtcSubjectLocator, HtcSubjectLocatorAdmin)
