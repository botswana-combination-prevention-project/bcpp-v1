from base_identifier import BaseIdentifier


class SubjectIdentifier(BaseIdentifier):

    def get_identifier_prep(self, **kwargs):
        """Changes the identifier model and format for subject identifiers."""
        options = {}
        options.update(app_name='bhp_identifier',
                       model_name='subject_identifier',
                       identifier_format='{prefix}-{site}{device_id}{sequence}')
        return options
