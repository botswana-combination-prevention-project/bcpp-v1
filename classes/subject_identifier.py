from base_subject_identifier import BaseSubjectIdentifier


class SubjectIdentifier(BaseSubjectIdentifier):

    def get_identifier_prep(self, **kwargs):
        """Changes the identifier model and format for subject identifiers."""
        custom_options = {}
        custom_options.update(
            app_name='bhp_identifier',
            model_name='subjectidentifier',
            identifier_format='{identifier_prefix}-{site_code}{device_id}{sequence}')
        return custom_options
