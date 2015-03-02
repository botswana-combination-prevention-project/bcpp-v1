from django.contrib import admin
from django.utils.translation import ugettext as _

from ..forms import ResidencyMobilityForm
from ..models import ResidencyMobility

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ResidencyMobilityAdmin(SubjectVisitModelAdmin):

    form = ResidencyMobilityForm

    baseline_fields = [
        "subject_visit",
        'length_residence',
        'permanent_resident',
        'intend_residency',
        'nights_away',
        'cattle_postlands',
        'cattle_postlands_other']

    annual_fields = [f for f in baseline_fields if f not in ['length_residence']]

    baseline_radio_fields = {
        "length_residence": admin.VERTICAL,
        "permanent_resident": admin.VERTICAL,
        "intend_residency": admin.VERTICAL,
        "nights_away": admin.VERTICAL,
        "cattle_postlands": admin.VERTICAL}

    annual_radio_fields = {
        "permanent_resident": admin.VERTICAL,
        "intend_residency": admin.VERTICAL,
        "nights_away": admin.VERTICAL,
        "cattle_postlands": admin.VERTICAL}

    instructions = [
        _("<H5>Read to Participant</H5> <p>To start, I will be asking"
          " you some questions about yourself, your living"
          " situation, and about the people that you live with."
          " Your answers are very important to our research and"
          " will help us understand how to develop better health"
          " programs in your community. Some of these questions"
          " may be embarrassing and make you feel uncomfortable;"
          " however, it is really important that you give the most"
          " honest answer that you can. Please remember that all of "
          " your answers are confidential. If you do not wish to "
          " answer, you can skip any question.</p>")]

admin.site.register(ResidencyMobility, ResidencyMobilityAdmin)
