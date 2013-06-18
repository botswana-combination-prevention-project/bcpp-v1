from django.core.exceptions import ValidationError


def select_field_true (value):
    if value :
        raise ValidationError(u'Date of birth cannot be a future date. You entered %s.' % value)
    
def start_with_model(value):
    if not value.startswith('Model.'):
        raise ValidationError('Query Set \'{0}\' should start with \'Model.\''.format(value))