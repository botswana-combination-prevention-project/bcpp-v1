from bhp_crypto.classes import BaseCrypter


def mask_encrypted(value):
    base_crypter = BaseCrypter()
    return base_crypter.mask(value)
