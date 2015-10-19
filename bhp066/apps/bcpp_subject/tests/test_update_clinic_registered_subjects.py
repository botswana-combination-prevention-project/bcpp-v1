from django.utils.unittest.case import TestCase
from django.db.models import Q

from bhp066.apps.bcpp_household_member.tests.factories.household_member_factory import HouseholdMemberFactory
from bhp066.apps.bcpp_household.tests.factories.household_structure_factory import HouseholdStructureFactory
from edc.subject.registration.tests.factories.registered_subject_factory import RegisteredSubjectFactory
from edc.subject.registration.models.registered_subject import RegisteredSubject
from bhp066.apps.bcpp_household.tests.factories.household_factory import HouseholdFactory
from bhp066.apps.bcpp_household.tests.factories.plot_factory import PlotFactory
from bhp066.apps.bcpp_household_member.models.household_member import HouseholdMember
from ..classes import ClinicRegisteredSubjectHelper


class TestUpdateClinicRegisteredSubjects(TestCase):
    
    
    def setUp(self):
        for _ in range(2):
            RegisteredSubjectFactory(identity='317918515')
        
        registered_subject = RegisteredSubject.objects.all()[0]
        household_structure = HouseholdStructureFactory()
        HouseholdMemberFactory(registered_subject=registered_subject, household_structure=household_structure)
        
        registered_subject = RegisteredSubject.objects.all()[1]
        plot = PlotFactory(status='bcpp_clinic', plot_identifier='160000-00')
        household = HouseholdFactory(plot=plot)
        household_structure = HouseholdStructureFactory(household=household)
        HouseholdMemberFactory(registered_subject=registered_subject, household_structure=household_structure)
        self.clinic_helper = ClinicRegisteredSubjectHelper()
    
    def test_find_duplicates(self):
        self.assertTrue(self.clinic_helper.find_duplicates())
        
    def test_determine_bcpp_registered_subject(self):
        bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
        hhm = HouseholdMember.objects.filter(registered_subject=bcpp_reg)
        self.assertEqual(hhm.household_structure.household.plot.status, 'residential_habitable')
        
        
    def test_clinic_household_member(self):
        bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
        self.clinic_member = None
        try:
            self.clinic_member = HouseholdMember.objects.get(
                Q(registered_subject__identity=bcpp_reg.identity),
                Q(household_structure__household__plot__status='bcpp_clinic')
            )
        except HouseholdMember.DoesNotExist:
            pass
        self.assertTrue(self.clinic_member)
        
    def test_update_clinic_household_member(self):
        bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
        self.clinic_member = None 
        try:
            self.clinic_member = HouseholdMember.objects.get(
                Q(registered_subject__identity=bcpp_reg.identity),
                Q(household_structure__household__plot__status='bcpp_clinic')
            )
            self.assertNotEqual(self.clinic_member.registered_subject.id, bcpp_reg.id)
        except HouseholdMember.DoesNotExist:
            pass
        
        self.clinic_helper.update_clinic_household_member(bcpp_reg)
        
        try:
            self.clinic_member = HouseholdMember.objects.get(
                Q(registered_subject__identity=bcpp_reg.identity),
                Q(household_structure__household__plot__status='bcpp_clinic')
            )
            self.assertEqual(self.clinic_member.registered_subject.id, bcpp_reg.id)
        except HouseholdMember.DoesNotExist:
            pass
    
    def test_clinic_appointment(self):
        pass
    