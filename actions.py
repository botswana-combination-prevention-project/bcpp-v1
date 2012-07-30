from bhp_crypto.classes import ModelCryptor


def encrypt(modeladmin, request, queryset, **kwargs):
    """ Encrypt a selection of instances that uses the EncryptedField object for any of its field objects """
    model_cryptor = ModelCryptor()
    for qs in queryset:
        model_cryptor.encrypt_instance(qs)
        #qs.save()
encrypt.short_description = "Encrypt a model that has \'Encrypted\' Fields"


def decrypt(modeladmin, request, queryset, **kwargs):
    """ Encrypt a selection of instances that uses the EncryptedField object for any of its field objects """
    model_cryptor = ModelCryptor()
    for qs in queryset:
        model_cryptor.decrypt_instance(qs)
        qs.save()
decrypt.short_description = "Decrypt a model that has \'Encrypted\' Fields (requires private key)"
