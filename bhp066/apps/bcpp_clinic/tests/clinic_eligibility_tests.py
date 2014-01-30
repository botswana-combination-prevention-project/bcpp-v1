from datetime import date, timedelta
from django.core.exceptions import ValidationError

from django.test import SimpleTestCase

from .factories import ClinicEligibilityFactory


class ClinicEligibilityTests(SimpleTestCase):
    
        def test_age_cannot_be_future_date(self):
            try:
                age_today = date.today()+timedelta(days=2)
                clinic_eligibility = ClinicEligibilityFactory(dob=age_today)
                fail('should have failed')
            except ValidationError as ve:
                print str(ve)
                self.assertEqual(ve.message, "Date of birth cannot be a future date. You entered %s.")

# 
#     def test_age_cannot_be_today(self):
#         "if participant age is set to today"
#         data = {'dob': date.today()}
#         clinic_eligibility_factory = ClinicEligibilityFactory()
#         clinic_eligibility_factory.clean = data
#         self.assertRaises(ValidationError, 'birth', clinic_eligibility_factory.clean())
  
#      def test_participant_underage(self):
#          "if participant is underage, ineligible"
#          form = ClinicEligibilityForm()
#          form.cleaned_data = {
#              'dob': '1999-11-20'}
#          self.assertRaisesMessage(ValidationError, 'Participant is below 16. Is not eligible', form.clean)
#          
#      
#      def test_participant_overage(self):
#          "if participant is overage, ineligible"
#          form = ClinicEligibilityForm()
#          form.cleaned_data = {
#              'dob': '1946-11-20'}
#          self.assertRaisesMessage(ValidationError, 'Participant is over 65. NOT eligible', form.clean)
#  
#  
#      def test_participant_residency(self):
#          "participant resides in community"
#          form = ClinicEligibilityForm()
#          form.cleaned_data = {
#              'part_time_resident': 'No'}
#          self.assertRaisesMessage(ValidationError, 'Participant does not live in this community. Spents less than 3nights. INELIGIBLE', form.clean)
