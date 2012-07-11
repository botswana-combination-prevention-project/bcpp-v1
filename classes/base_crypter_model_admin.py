from bhp_base_model.classes import BaseModelAdmin
from bhp_crypto.actions import encrypt, decrypt
from bhp_crypto.classes import BaseEncryptedField


class BaseCrypterModelAdmin (BaseModelAdmin):
    
    """Overide ModelAdmin to force username to be saved on add/change and other stuff""" 
    def __init__(self, *args, **kwargs):
        #add cypter actions
        self.actions.append(encrypt)    
        self.actions.append(decrypt)                               
        super(BaseCrypterModelAdmin, self).__init__(*args, **kwargs)

    def get_readonly_fields(self, request, obj = None):
        
        super(BaseCrypterModelAdmin, self).get_readonly_fields(request, obj)

        # make crypter fields readonly if no private key and in edit mode
        if obj: #In edit mode
            for field in obj._meta.fields:
                if isinstance(field, BaseEncryptedField):
                    if not field.have_decryption_key() and field.attname not in self.readonly_fields:
                        self.readonly_fields = (field.attname,) + self.readonly_fields 
        return self.readonly_fields
