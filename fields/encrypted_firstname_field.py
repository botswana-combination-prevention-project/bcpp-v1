from weak_encryption_field import WeakEncryptionField
from django.forms import ValidationError


class EncryptedFirstnameField(WeakEncryptionField):
    
    def validate_with_cleaned_data(self, attrname, cleaned_data):
        
        value = cleaned_data.get('first_name', None)