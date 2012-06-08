from bhp_crypto.classes import ModelCrypter


def encrypt(modeladmin, request, queryset, **kwargs):
    """ Encrypt a selection of instances that uses the EncryptedField object for any of its field objects """
    model_crypter = ModelCrypter()
    for qs in queryset: 
        model_crypter.encrypt_instance(qs)
        qs.save()
            
encrypt.short_description = "Encrypt a model that has \'Encrypted\' Fields"

def decrypt(modeladmin, request, queryset, **kwargs):
    """ Encrypt a selection of instances that uses the EncryptedField object for any of its field objects """
    model_crypter = ModelCrypter()
    for qs in queryset: 
        model_crypter.decrypt_instance(qs)
        qs.save()
    
decrypt.short_description = "Decrypt a model that has \'Encrypted\' Fields (requires private key)"