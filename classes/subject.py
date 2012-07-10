from bhp_variables.models import StudySpecific
from bhp_device.classes import Device
from bhp_identifier.models import SubjectIdentifier
from check_digit import CheckDigit
from base import Base


class Subject(Base):
    
    """ Create the subject identifier by calling get_identifier() """
    
    def __init__(self):
        # these are passed via the get_identifier method
        self.subject_type = None
        self.site = None
        # these come from static sources
        study_specific = StudySpecific.objects.all()[0]
        self.modulus = study_specific.subject_identifier_modulus
        self.seed = str(study_specific.subject_identifier_seed)
        self.prefix = study_specific.subject_identifier_prefix
    
    def get_identifier(self, subject_type, site, **kwargs):
        """ given the subject type and study site code, return a formatted identifier 
        Format is {prefix}-{site}{device_id}{sequence}-{check_digit}"""
        # create/save a new SubjectIdentifier model instance to get a unique sequence
        subject_identifier = SubjectIdentifier.objects.create(seed=self.seed)
        # get the device id (usually 2 digits)
        device = Device() 
        # format the base string
        base = "{prefix}-{site}{device_id}{sequence}".format(prefix = self.prefix, 
                                                             site = site,
                                                             device_id = device.device_id,
                                                             sequence = subject_identifier.sequence)
        # add a check digit and set the SubjectIdentifier model instance attribute
        check_digit = CheckDigit()
        subject_identifier.subject_identifier = "{base}-{check_digit}".format(base = base, 
                                                           check_digit = check_digit.calculate(int(base.replace('-','')),
                                                           self.modulus))    
        # re-save the SubjectIdentifier model instance
        subject_identifier.save()
        # set this instance attribute to the identifier string
        self.subject_identifier = subject_identifier.subject_identifier
        # return just the attribute value
        return self.subject_identifier
                                                                                                                                                       
    
                

        
