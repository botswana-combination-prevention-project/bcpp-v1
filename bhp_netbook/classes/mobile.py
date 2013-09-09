#from django.db.models import get_model
#from bhp_device.classes import Device
#from bhp_netbook.models import MobileDataTracker
#
#
#class Mobile(object):
#
#    def clear(self):
#        """ """
#        pass
#
#    def import_household(self, identifier, mobile_device):
#        from mochudi_household.models import HouseholdStructureMember, HouseholdStructure, Household
#        household = self.check_out(Household, identifier)
#        if household:
#            self.import_data_component(self, household, mobile_device)
#
#    def check_out(self, cls, identifier):
#        """Checks out a household and all its members form the master."""
#        # does object exist in survey?
#        if not cls.objects.filter(household_identifier=identifier).exists():
#            raise ValueError('A {0} with identifier {1} not found.'.format(cls._meta.object_name, identifier))
#        # is anyone using cls instance
#        if MobileDataTracker.objects.filter(identifier=identifier, status='out').exists():
#            data_tracker = MobileDataTracker.objects.get(identifier=identifier, status='out')
#            raise ValueError('Household with identifier {0} is currently in use by {0}.'.format(data_tracker.data_tracker_user))
#        household = cls.objects.get(household_identifier=identifier)
#        #check_out
#        device = Device()
#        defaults = {'status': 'out', 'data_tracker_user': device.device_id}
#        data_tracker, created = MobileDataTracker.objects.get_or_create(identifier=identifier, defaults=defaults)
#        if not created:
#            data_tracker.status = 'out'
#            data_tracker.save()
#        return household
#
#    def check_in(self, identifier):
#        """Checks out a data component."""
#        pass
#
#    def send_data_component(self, household, mobile_device):
#        """Override"""
#        from mochudi_household.models import HouseholdStructureMember, HouseholdStructure, Household
#        survey = ''
#        #build an import plan
#        models = [('mochudi_household', 'household'), ('mochudi_household', 'householdstructure'), ('mochudi_household', 'householdstructuremember')]
#        for app_label, model_name in models:
#            new_instance = self.copy_instance(get_model(app_label, model_name))
#            new_instance.save(using=mobile_device)
#            
#        #add structure for this survey
#        
#        #add members
#        
#        #update status hiv status and participation status
#        
#        # update registered subject data for all subjects
#        for household_structure_member in HouseholdStructureMember.objects.filter(household_structure__household__identifier=household.identifier):
#            household_structure_members = 
#            
#        # get hs for this survey
#        # if it does not exist, create it
#        if HouseholdStructure
#        
#
#        # what is the outer child model?
#        outer_child = 'HouseholdStructureMember'
#        # get all relation  
#
#    def copy_instance(self, instance):
#        """Copies an instance."""
#        new_instance = instance.__class__()
#        for field in instance._meta.fields:
#            if field.name not in ['id']:
#                setattr(instance, field.name, getattr(instance, field.name))
#        return new_instance
