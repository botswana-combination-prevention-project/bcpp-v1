from base_subject_identifier import BaseSubjectIdentifier


class SubjectIdentifier(BaseSubjectIdentifier):

    def __init__(self, identifier_format=None, app_name=None, model_name=None, site_code=None, padding=None, modulus=None, identifier_prefix=None, using=None):
        identifier_format = '{identifier_prefix}-{site_code}{device_id}{sequence}'
        app_name = 'bhp_identifier'
        model_name = 'subjectidentifier'
        super(SubjectIdentifier, self).__init__(identifier_format, app_name, model_name, site_code, padding, modulus, identifier_prefix, using)
