import socket
from django.db import models
from django.db.models import Max
from bhp_variables.models import StudySpecific
from bhp_netbook.models import Netbook


class HouseholdManager(models.Manager):

    def get_by_natural_key(self, household_identifier):
        return self.get(household_identifier=household_identifier)

    def get_identifier(self):

        """
        Generates a household identifier by incrementing the seed for a given device id

        households = Household.objects.all()
        for household in households:
            household.device_id=household.household_identifier[1:3]
            household.save()
        """

        if super(HouseholdManager, self).filter(device_id__isnull=True):
            households = super(HouseholdManager, self).filter(device_id__isnull=True)
            for household in households:
                household.device_id = household.household_identifier[1:3]
                household.save()
        study_variables = StudySpecific.objects.all()[0]
        if Netbook.objects.filter(name=socket.gethostname()):
            # assume device id is char 3-5
            device_id = Netbook.objects.get(name=socket.gethostname()).name[3:5]
            try:
                int(device_id)
            except:
                raise TypeError('Device id must be an integer (characters 3-5 of hostname). '
                                ' Got {0}'.format(device_id))
        elif study_variables.device_id >= 10 and study_variables.device_id <= 99:
            device_id = str(study_variables.device_id)
        elif study_variables.device_id == 0:
            #TODO: ensure last two characters of the servername are unique and an integer in bhp_variables
            device_id = socket.gethostname()[-2:]
            try:
                int(device_id)
            except:
                raise TypeError('Failed to convert last two digits of \'Server\''
                                'hostname {0} to integer, Got {1}'.format(socket.gethostname().name, device_id))
        else:
            raise TypeError("Cannot determine a 2-digit device_id from hostname NOR bhp_variables.")
        aggr = super(HouseholdManager, self).filter(device_id=device_id).aggregate(Max('hh_seed'))
        if aggr['hh_seed__max']:
            seed = aggr['hh_seed__max'] + 1
            id_int = int(device_id + str(seed))
        else:
            seed = study_variables.subject_identifier_seed + 1
            id_int = int(device_id + str(seed))
        check_digit = id_int % 103
        while check_digit > 99:
            id_int = id_int + 1
            seed = seed + 1
            check_digit = id_int % 103
        household_identifier = {}
        #set ID, format is H9999-000 (pad x with 0's)
        if check_digit < 10:
            household_identifier['id'] = "H%s-0%s" % (id_int, check_digit)
        if check_digit >= 10 and check_digit < 100:
            household_identifier['id'] = "H%s-%s" % (id_int, check_digit)
        household_identifier['hh_seed'] = seed
        household_identifier['hh_int'] = id_int
        return household_identifier
