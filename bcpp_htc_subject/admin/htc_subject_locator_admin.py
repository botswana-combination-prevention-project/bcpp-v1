from django.contrib import admin
from bcpp_htc_subject.models import HtcSubjectLocator
from bcpp_htc_subject.forms import HtcSubjectLocatorForm
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin


class HtcSubjectLocatorAdmin(HtcSubjectVisitModelAdmin):

    form = HtcSubjectLocatorForm

admin.site.register(HtcSubjectLocator, HtcSubjectLocatorAdmin)
