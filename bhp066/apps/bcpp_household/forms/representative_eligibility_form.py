from django.db.models import Max
from django.forms import ValidationError

from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..constants import ELIGIBLE_REPRESENTATIVE_ABSENT
from ..models import RepresentativeEligibility, HouseholdLogEntry


class RepresentativeEligibilityForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(RepresentativeEligibilityForm, self).clean()
        household_structure = cleaned_data.get('household_structure')
        try:
            report_datetime = HouseholdLogEntry.objects.filter(
                household_log__household_structure=household_structure).aggregate(
                    Max('report_datetime')).get('report_datetime__max')
            if HouseholdLogEntry.objects.get(
                    household_log__household_structure=household_structure,
                    household_status='no_household_informant',
                    report_datetime=report_datetime):
                raise ValidationError('You cannot save representative eligibility, no household informant.')

            HouseholdLogEntry.objects.get(
                household_log__household_structure=household_structure,
                report_datetime=report_datetime,
                household_status=ELIGIBLE_REPRESENTATIVE_ABSENT)
            raise ValidationError('The eligible household representative is absent. See Household Log.')
        except HouseholdLogEntry.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = RepresentativeEligibility
