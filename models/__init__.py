from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_variables.models import StudySpecific
from subject_identifier_audit_trail import *
from base_randomization_list import *
from registered_subject import RegisteredSubject
from base_registered_subject_model import BaseRegisteredSubjectModel
from base_registration_model import BaseRegistrationModel
from signals import *

if not 'MAX_SUBJECTS' in dir(settings):
    raise ImproperlyConfigured('Missing settings attribute MAX_SUBJECTS. Please add settings attribute MAX_SUBJECTS = to your settings file.')
# else:
#     subject_types = StudySpecific.objects.all()[0].subject_type.split(',')
#     if len(subject_types) > 1