from base_subject_identifier import BaseSubjectIdentifier


class SubjectIdentifier(BaseSubjectIdentifier):

    def get_identifier_prep(self, **kwargs):
        """Changes the identifier model and format for subject identifiers."""
        options = {}
        options.update(app_name='bhp_identifier',
                       model_name='subjectidentifier',
                       identifier_format='{prefix}-{site}{device_id}{sequence}')
        return options
