import factory
from datetime import date
from django.conf import settings
from bhp_base_model.tests.factories import BaseUuidModelFactory

starting_seq_num = 1000


class BaseSubjectFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    # if you set subject_identifier here, filling in a consent, for example, will not generate 
    # an identifier and not update registered subject
    #subject_identifier = factory.Sequence(lambda n: '{0}-{1}{2}-0'.format(settings.PROJECT_IDENTIFIER_PREFIX, settings.DEVICE_ID, n.rjust(5, '0')))
    first_name = 'ERIK'
    initials = 'EV'
    dob = date(date.today().year - 20, 1, 1)
    is_dob_estimated = '-'
    gender = 'M'
    subject_type = 'subject'
