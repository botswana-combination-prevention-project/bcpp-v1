import os
from datetime import datetime
from bhp_crypto.classes.hasher import Hasher
from bhp_crypto.fields.restricted_rsa_encryption_field import RestrictedRsaEncryptionField
from bhp_crypto.fields.local_rsa_encryption_field import LocalRsaEncryptionField
from bhp_crypto.fields.local_aes_encryption_field import LocalAesEncryptionField

def setup_new_keys():

    datestring = datetime.today().strftime('%Y%m%d%H%M%S%f')
    pem = {'restricted_public': 'user-public-restricted.pem',
           'restricted_private': 'user-private-restricted.pem',
           'local_public': 'user-public-local.pem',
           'local_private': 'user-private-local.pem',
           'local-aes': 'user-aes-local',}
    # backup existing keys
    try:
        path='keys_backup_{0}'.format(datestring)
        os.mkdir(path)
        print path
    except:
        raise TypeError('failed to create backup folder')    
    

    for filename in pem.itervalues():
        try:
            oldpath=os.path.join(os.path.realpath('.'),filename)
            newpath=os.path.join(os.path.join(os.path.realpath('.'),path), filename)
            print filename
            os.rename(oldpath, newpath)
        except:
            print 'Failed to copy {0} to backup folder {1}'.format(filename, path)
    
    #create restricted RSA
    fld = RestrictedRsaEncryptionField()
    fld.crypter.create_new_key_pair()
    # create local RSA
    fld = LocalRsaEncryptionField()
    fld.crypter.create_new_key_pair()
    #create and encrypt a salt
    hasher=Hasher()
    hasher.set_public_key(pem.get('local_public'))
    #create and encrypt AES key
    fld=LocalAesEncryptionField()
    fld.crypter.create_aes_key(pem.get('local_public'))

   
