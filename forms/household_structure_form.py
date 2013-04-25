from datetime import datetime
from django import forms
from django.conf import settings
#from bhp_dispatch.helpers import is_dispatched
from bcpp_household.models import HouseholdStructure


class HouseholdStructureForm(forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        #check if dispatched
        household = cleaned_data.get('household', None)
        if household:
            if household.is_dispatched_as_item():
                raise forms.ValidationError("Household is currently dispatched. Data may not be changed.")
        # check survey is current survey
        if cleaned_data.get('survey'):
            if hasattr(settings, 'ALLOW_CHANGES_OTHER_SUVERYS') and settings.ALLOW_CHANGES_OTHER_SUVERYS:
                pass
            else:
                if not cleaned_data.get('survey').datetime_start <= datetime.today() or not datetime.today() <= cleaned_data.get('survey').datetime_end:
                    raise forms.ValidationError('%s is not the current survey. You may only add/change data for the current survey' % (cleaned_data.get('survey').survey_name, ))

        return cleaned_data

    class Meta:
        model = HouseholdStructure
